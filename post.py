import os
import time
import random
from instagrapi import Client
from instagrapi.exceptions import ChallengeRequired
from datetime import datetime

# Configuration
FOLDER_PATH = "reels"
TEST_REEL = "test_reel.mp4"
SESSION_FILE = "session.json"  # For persistent login

def get_client():
    client = Client()
    creds = os.getenv("SECRETS")
    
    if not creds:
        print("🔴 SECRETS environment variable missing!")
        exit()
    
    try:
        username, password = creds.split(":")
        
        # Try loading existing session first
        if os.path.exists(SESSION_FILE):
            client.load_settings(SESSION_FILE)
            try:
                client.get_timeline_feed()  # Test session
                print("🔑 Session loaded successfully")
                return client
            except Exception:
                print("🔄 Session expired - Re-authenticating...")
                os.remove(SESSION_FILE)
        
        # New login with 2FA handling
        try:
            client.login(username, password)
            print("🔑 Login successful")
        except ChallengeRequired:
            print("\n🔐 2FA Verification Required!")
            print("1. Check your email/SMS for Instagram code")
            print("2. Enter the 6-digit code below")
            code = input(">> ").strip()
            client.challenge_code(code)
            
        client.dump_settings(SESSION_FILE)  # Save session
        return client
        
    except Exception as e:
        print(f"🔴 Login failed: {str(e)}")
        exit()

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
    client = get_client()  # Handles both normal and 2FA login
    
    # Main loop with random intervals (5-10 mins)
    while True:
        delay = random.randint(300, 600)
        next_post = datetime.now().timestamp() + delay
        
        print(f"\n🕒 Next post at {datetime.fromtimestamp(next_post).strftime('%H:%M:%S')}")
        post_reel(client)
        
        print(f"⏳ Waiting {delay//60} minutes...")
        time.sleep(delay)

if __name__ == "__main__":
    main()
