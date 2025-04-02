import os
import time
from instagrapi import Client
from datetime import datetime

# Configuration (Test Mode)
FOLDER_PATH = "reels"  # Folder with reels
TEST_REEL = "test_reel.mp4"  # Name of your test video file
INTERVAL = 300  # 5 minutes (in seconds)

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
    
    # Simplified login (no session saving)
    try:
        client.login(os.getenv("INSTA_USER"), os.getenv("INSTA_PASS"))
        print("🔑 Login successful")
    except Exception as e:
        print(f"🔴 Login failed: {str(e)}")
        return

    # Test loop
    while True:
        print(f"\n🕒 Attempting test post at {datetime.now().strftime('%H:%M:%S')}")
        post_reel(client)
        print(f"⏳ Next attempt in {INTERVAL//60} minutes...")
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
