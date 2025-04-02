import os
import time
import random
from instagrapi import Client
from datetime import datetime

# Configuration
FOLDER_PATH = "reels"
TEST_REEL = "test_reel.mp4"

def post_reel(client):
    reel_path = os.path.join(FOLDER_PATH, TEST_REEL)
    if not os.path.exists(reel_path):
        print(f"❌ Test reel not found at: {reel_path}")
        return False
    
    try:
        client.clip_upload(
            path=reel_path,
            caption=f"TEST POST - {datetime.now().strftime('%H:%M:%S')}",
            thumbnail=None
        )
        print("✅ Test post successful!")
        return True
    except Exception as e:
        print(f"❌ Post failed: {str(e)}")
        return False

def main():
    client = Client()
    
    # Login with SECRETS
    try:
        creds = os.getenv("SECRETS")
        if not creds:
            print("🔴 SECRETS not found in environment variables!")
            return
        username, password = creds.split(":")
        client.login(username, password)
        print("🔑 Login successful")
    except Exception as e:
        print(f"🔴 Login failed: {str(e)}")
        return

    # Main loop with random intervals (300-600 seconds = 5-10 mins)
    while True:
        delay = random.randint(300, 600)  # Random delay between 5-10 minutes
        next_post = datetime.now().timestamp() + delay
        
        print(f"\n🕒 Next post at {datetime.fromtimestamp(next_post).strftime('%H:%M:%S')}")
        post_reel(client)
        
        print(f"⏳ Waiting {delay//60} minutes...")
        time.sleep(delay)

if __name__ == "__main__":
    main()
