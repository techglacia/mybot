import os
from instagrapi import Client
from instagrapi.exceptions import ChallengeRequired

def get_client():
    client = Client()
    creds = os.getenv("SECRETS")
    username, password = creds.split(":")
    
    try:
        # Try normal login first
        client.login(username, password)
    except ChallengeRequired:
        print("\n🔐 2FA Required! Using backup code...")
        # Method 1: Use backup code (generate in Instagram settings)
        client.login(username, password, verification_code="YOUR_BACKUP_CODE")
        
        # OR Method 2: For testing, disable 2FA temporarily
        # client.login(username, password, verification_code="")
    
    return client

# Usage
client = get_client()
