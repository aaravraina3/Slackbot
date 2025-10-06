#!/usr/bin/env python3
"""
Improved email lookup with fallbacks and better error handling
"""

from bot.config import load_config
from bot.slack import get_slack_client, lookup_user_by_email

def lookup_user_with_fallbacks(client, northeastern_email, personal_email, first_name, last_name):
    """
    Try multiple ways to find a user in Slack
    """
    print(f"🔍 Looking up {first_name} {last_name}...")
    
    # Try Northeastern email first
    if northeastern_email:
        print(f"  Trying Northeastern email: {northeastern_email}")
        user_id = lookup_user_by_email(client, northeastern_email)
        if user_id:
            print(f"  ✅ Found via Northeastern email: {user_id}")
            return user_id
    
    # Try personal email
    if personal_email:
        print(f"  Trying personal email: {personal_email}")
        user_id = lookup_user_by_email(client, personal_email)
        if user_id:
            print(f"  ✅ Found via personal email: {user_id}")
            return user_id
    
    # Try common email variations
    email_variations = [
        f"{first_name.lower()}.{last_name.lower()}@northeastern.edu",
        f"{first_name.lower()}{last_name.lower()}@northeastern.edu", 
        f"{last_name.lower()}.{first_name.lower()}@northeastern.edu",
        f"{first_name.lower()}{last_name[0].lower()}@northeastern.edu",
    ]
    
    for email in email_variations:
        if email not in [northeastern_email, personal_email]:  # Don't try duplicates
            print(f"  Trying variation: {email}")
            user_id = lookup_user_by_email(client, email)
            if user_id:
                print(f"  ✅ Found via variation: {user_id}")
                return user_id
    
    print(f"  ❌ Could not find {first_name} {last_name} in Slack")
    return None

def test_lookup_people():
    """Test lookup for Aarav and Neha only - NO MESSAGES SENT"""
    client = get_slack_client()
    
    print("🔍 Testing lookup for Aarav and Neha only...\n")
    
    # Test Aarav
    print("=== AARAV RAINA ===")
    aarav_id = lookup_user_with_fallbacks(
        client, 
        "raina.aa@northeastern.edu", 
        "", 
        "Aarav", 
        "Raina"
    )
    
    print("\n=== NEHA JHA ===")
    neha_id = lookup_user_with_fallbacks(
        client,
        "jha.ne@northeastern.edu",
        "nehajha2004@gmail.com", 
        "Neha",
        "Jha"
    )
    
    print(f"\n📊 Results:")
    print(f"✅ Aarav: {'Found' if aarav_id else 'Not found'}")
    print(f"✅ Neha: {'Found' if neha_id else 'Not found'}")
    
    print("\n🚫 NO MESSAGES SENT - TESTING ONLY")

if __name__ == "__main__":
    test_lookup_people()
