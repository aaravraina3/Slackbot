#!/usr/bin/env python3
"""
Create the Tracking sheet for the feedback bot
"""

from bot.config import load_config
from bot.sheets import connect_to_sheets

def create_tracking_sheet(service, spreadsheet_id):
    """Create the Tracking sheet with headers"""
    
    # Create the Tracking sheet
    print("Creating Tracking sheet...")
    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={
            'requests': [{
                'addSheet': {
                    'properties': {
                        'title': 'Tracking'
                    }
                }
            }]
        }
    ).execute()
    
    # Add header row
    header = [['Email', 'Team', 'Date_Selected', 'Form_Completed', 'Reminders_Sent', 'Date_Completed']]
    
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range='Tracking!A1:F1',
        valueInputOption='USER_ENTERED',
        body={'values': header}
    ).execute()
    
    print("Created Tracking sheet with headers")

def main():
    cfg = load_config()
    service = connect_to_sheets(cfg.google_creds_path)
    
    create_tracking_sheet(service, cfg.google_sheets_id)
    print("Done! Now you can test the bot with:")
    print("python3 -m scripts.test_dry_run")

if __name__ == "__main__":
    main()
