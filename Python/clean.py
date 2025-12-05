from bs4 import BeautifulSoup
import pandas as pd
import os 

from config import OUTPUT_PATH, Cleaned_OUTPUT_PATH



def strip_html(content: str) -> str:
    
    if pd.isna(content):
        return ""
    
    return BeautifulSoup(content, "html.parser").get_text(separator=" ")
   
def main():
    
    print("Loading scraped data...")
    df = pd.read_csv(OUTPUT_PATH)
    print("Loaded:", df.shape)
    
    print("Stripping HTML from content...")
    df["content_text"] = df["content_html"].apply(strip_html)
    df = df[df["content_text"].str.strip().str.len() > 0]
    df = df.drop(columns=["content_html"])

    print("After stripping HTML:", df.shape)
    
    print("Saving cleaned data...",)
    df.to_csv(Cleaned_OUTPUT_PATH, index=False, encoding="utf-8")
    
    print("Done. Cleaned data shape:", df.shape)
    print("Saved cleaned data to", Cleaned_OUTPUT_PATH)
    
    
    
if __name__ == "__main__":
    main()