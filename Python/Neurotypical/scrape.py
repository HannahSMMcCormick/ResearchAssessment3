
import os
import pandas as pd
from dotenv import load_dotenv
from mastodon import Mastodon
from config import OUTPUT_PATH, Env


def init_mastodon():

    # Load environment variables from .env file
    load_dotenv(dotenv_path=Env)  

    # Initialize Mastodon client
    # Get credentials from environment variables
    base_url = os.getenv("MASTODON_BASE_URL")
    access_token = os.getenv("MASTODON_ACCESS_TOKEN")

    # Check if credentials are available
    if not base_url or not access_token:
        raise RuntimeError(
            "MASTODON_BASE_URL or MASTODON_ACCESS_TOKEN not set in .env"
        )

    # Initialize Mastodon client
    mastodon = Mastodon(
        api_base_url=base_url,
        access_token=access_token,
    )
    return mastodon


def scrape_public_timeline(mastodon: Mastodon, limit: int = 500):

    # List to store collected posts
    posts = []

    # Initialize counters for fetched posts and pagination
    fetched = 0
    max_id = None


    # Loop to fetch posts until the limit is reached
    while fetched < limit:
        # Fetch a batch of posts with the specified hashtag
        batch = mastodon.timeline_public(
            limit=min(40, limit - fetched),  
            max_id=max_id,
        )
        if not batch:
            break

        # Process each post in the fetched batch
        for status in batch:
            # Skip reblogs
            if status.reblog:
                continue

            if status.language != "en":
                continue
            
            content_text = status.content 
           
            # Append post data to the list
            posts.append(
                {
                    "platform": "mastodon",
                    "status_id": status.id,
                    "created_at": status.created_at.isoformat(),
                    "account_id": status.account.id,
                    "account_name": status.account.acct,
                    "content_html": content_text,
                    "url": status.url,
                    "replies_count": status.replies_count,
                    "reblogs_count": status.reblogs_count,
                    "favourites_count": status.favourites_count,
                    "sensitive": status.sensitive,
                    "visibility": status.visibility,
                }
            )
            # Increment the fetched counter
            fetched += 1
            if fetched >= limit:
                break
        # Update max_id for pagination        
        max_id = batch[-1].id

    return posts

def main():
    mastodon = init_mastodon()
    print("Scraping public timeline...")

    posts = scrape_public_timeline(mastodon, limit=3900)
    print(f"Collected {len(posts)} public posts.")

    # Check if any posts were collected
    if not posts:
        print("No posts collected. Check credentials and hashtags.")
        return

    # Create DataFrame from collected posts
    df = pd.DataFrame(posts)

    # Remove duplicate posts based on status_id
    df = df.drop_duplicates(subset=["status_id"])

    # Save DataFrame to CSV
    os.makedirs("data", exist_ok=True)
    output_path = OUTPUT_PATH
    df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"Saved {len(df)} posts to {output_path}")

if __name__ == "__main__":
    main()
