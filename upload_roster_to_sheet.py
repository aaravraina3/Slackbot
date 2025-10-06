#!/usr/bin/env python3
"""
Upload roster data to Google Sheet
"""

import csv
from bot.config import load_config
from bot.sheets import connect_to_sheets

def convert_csv_to_roster(csv_file):
    """Convert the CSV to the Roster format expected by the bot"""
    
    roster_data = []
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            # Extract the data we need
            first_name = row.get('Northeastern First Name', '').strip()
            last_name = row.get('Last Name', '').strip()
            full_name = f"{first_name} {last_name}".strip()
            
            # Try Northeastern email first, then personal
            email = row.get('Northeastern Email Address', '').strip()
            if not email:
                email = row.get('Personal Email Address', '').strip()
            
            # Get team info
            team = row.get('Which team are you a part of?', '').strip()
            if team:
                # Clean up team names
                team = team.replace(':', '').strip()
                if team.lower() in ['data', 'data unsprawl']:
                    team = 'data'
                elif team.lower() in ['software', 'software unsprawl']:
                    team = 'software'
                elif team.lower() in ['design', 'design unsprawl']:
                    team = 'design'
                elif team.lower() in ['marketing', 'marketing unsprawl']:
                    team = 'marketing'
                elif team.lower() in ['operations', 'ops', 'operations unsprawl']:
                    team = 'operations'
                else:
                    team = team.lower()
            
            # Only include if we have essential data
            if full_name and email and team:
                roster_data.append([full_name, email, team, 'Active'])
    
    return roster_data

def upload_roster(service, spreadsheet_id, roster_data):
    """Upload roster data to Google Sheet"""
    
    # First, try to create the Roster sheet if it doesn't exist
    try:
        # Try to read from Roster sheet to see if it exists
        service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range='Roster!A1'
        ).execute()
    except:
        # If it doesn't exist, create it
        print("Creating Roster sheet...")
        service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={
                'requests': [{
                    'addSheet': {
                        'properties': {
                            'title': 'Roster'
                        }
                    }
                }]
            }
        ).execute()
    
    # Add header row
    header = [['Name', 'Email', 'Team', 'Status']]
    
    # Upload header
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range='Roster!A1:D1',
        valueInputOption='USER_ENTERED',
        body={'values': header}
    ).execute()
    
    # Upload roster data
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range='Roster!A2:D' + str(len(roster_data) + 1),
        valueInputOption='USER_ENTERED',
        body={'values': roster_data}
    ).execute()
    
    print(f"Uploaded {len(roster_data)} members to Google Sheet")

def main():
    cfg = load_config()
    service = connect_to_sheets(cfg.google_creds_path)
    
    csv_file = 'Slackbot copy F25 Generate Onboarding Form (Responses) - Form responses 1.csv'
    
    print("Converting CSV to Roster format...")
    roster = convert_csv_to_roster(csv_file)
    
    print(f"Found {len(roster)} members")
    print("Uploading to Google Sheet...")
    
    upload_roster(service, cfg.google_sheets_id, roster)
    
    print("Done! Now you can test the bot with:")
    print("python -m scripts.test_dry_run")

if __name__ == "__main__":
    main()
