import os 
import pandas as pd
from textblob import TextBlob
from detoxify import Detoxify
from config import Results_OUTPUT_PATH, Cleaned_OUTPUT_PATH

def compute_sentiment(text:str):
    
    blob = TextBlob(text)
    return blob.sentiment.polarity, blob.sentiment.subjectivity

def add_sentiment_columns(df:pd.DataFrame):
    
    sentiments = df["content_text"].apply(compute_sentiment)
    df["sentiment_polarity"] = sentiments.apply(lambda x: x[0])
    df["sentiment_subjectivity"] = sentiments.apply(lambda x: x[1])
    return df


def compute_toxicity(df):
    print("Loading Detoxify model...")
    
    model = Detoxify('original')
    print("Model loaded. Computing toxicity...")
    preds = model.predict(df["content_text"].astype(str).tolist())
    
    for key, value in preds.items():
        df[f'toxicity_{key}'] = value
        
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
    