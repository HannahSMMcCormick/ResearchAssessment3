import os 
import pandas as pd
from textblob import TextBlob
from detoxify import Detoxify
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from config import Results_OUTPUT_PATH, Cleaned_OUTPUT_PATH

MODEL_NAME = "cardiffnlp/twitter-roberta-base-sentiment-latest"


def compute_sentiment():
    
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
    sent_pipe = pipeline("sentiment-analysis",
                         model=model, 
                         tokenizer=tokenizer,
                         truncation=True,
                         max_length=256,
                         device=-1,
                         return_all_scores=True)
    return sent_pipe

def add_sentiment_columns(df):
    
    print("Loading HuggingFace sentiment model...")
    sent_pipe = compute_sentiment()
    print("Model loaded. Computing sentiment...")
    
    
    sentiments = df["content_text"].astype(str).tolist()
    
    results = sent_pipe(sentiments, batch_size=32)
    labels = []
    polarities = []
    
    for res in results:
        
        scores = {item["label"].lower(): float(item["score"]) for item in res}

        # Try to get scores; default to 0 if label name is weird
        neg = next((v for k, v in scores.items() if "neg" in k), 0.0)
        pos = next((v for k, v in scores.items() if "pos" in k), 0.0)
        neu = next((v for k, v in scores.items() if "neu" in k), 0.0)

        # Simple polarity: positive minus negative
        polarity = pos - neg

        # Pick the label with the highest score as the categorical label
        top_label = max(scores, key=scores.get)

        labels.append(top_label)
        polarities.append(polarity)

    df["hf_sentiment_label"] = labels
    df["hf_sentiment_polarity"] = polarities

    print("Computing subjectivity (TextBlob)...")
    df["sentiment_subjectivity"] = df["content_text"].apply(
        lambda x: TextBlob(str(x)).sentiment.subjectivity
    )

    return df


def compute_toxicity(df,batch_size: int = 64):
    print("Loading Detoxify model...")
    
    model = Detoxify('unbiased')
    print("Model loaded. Computing toxicity...")

    
    texts = df["content_text"].astype(str).tolist()
    n = len(texts)
    all_scores = None

    for start in range(0, n, batch_size):
        end = min(start + batch_size, n)
        batch = texts[start:end]
        print(f"  Processing batch {start}–{end} of {n}...")

        batch_preds = model.predict(batch)  # dict: label -> list of scores

        if all_scores is None:
            # initialize dict of label -> list
            all_scores = {k: [] for k in batch_preds.keys()}

        for k, v in batch_preds.items():
            all_scores[k].extend(v)

    # Now attach to df
    for key, values in all_scores.items():
        df[f"toxicity_{key}"] = values

    return df

def main():
    
    print("Loading cleaned dataset from", Cleaned_OUTPUT_PATH)
    if not os.path.exists(Cleaned_OUTPUT_PATH):
        raise FileNotFoundError(f"Cleaned data file not found at {Cleaned_OUTPUT_PATH}. Please run the cleaning step first.")
    
    
    df = pd.read_csv(Cleaned_OUTPUT_PATH)
    print("Loaded:", df.shape)
    
    if "content_text" not in df.columns:
        print("Error: 'content_text' column not found in the dataset. Columns are:", list(df.columns))
        return
    
    df = add_sentiment_columns(df)
    print("Added sentiment columns.")
    
    df = compute_toxicity(df)
    print("Added toxicity columns.")
    
    print("Saving augmented dataset to:",Results_OUTPUT_PATH )
    df.to_csv(Results_OUTPUT_PATH, index=False, encoding="utf-8")
    
    print("Done. Final dataset shape:", df.shape)
    
    for col in df.columns:
        if col.startswith("sentiment_") or col.startswith("toxicity_"):
            print(f"  - {col}")
            
if __name__ == "__main__":
    main()
    