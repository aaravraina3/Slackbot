#!/usr/bin/env python3
"""
Add response tracking features to the Google Sheet
"""

from bot.config import load_config
from bot.sheets import connect_to_sheets

def add_response_tracking(service, spreadsheet_id):
    """Add response tracking sheets"""
    
    # Create "Reached Out" sheet
    print("Creating 'Reached Out' sheet...")
    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={
            'requests': [{
                'addSheet': {
                    'properties': {
                        'title': 'Reached Out'
                    }
                }
            }]
        }
    ).execute()
    
    # Add headers for Reached Out sheet
    reached_out_headers = [['Name', 'Email', 'Team', 'Date_Reached', 'Message_Sent', 'Slack_User_ID']]
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range='Reached Out!A1:F1',
        valueInputOption='USER_ENTERED',
        body={'values': reached_out_headers}
    ).execute()
    
    # Create "Responded" sheet
    print("Creating 'Responded' sheet...")
    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={
            'requests': [{
                'addSheet': {
                    'properties': {
                        'title': 'Responded'
                    }
                }
            }]
        }
    ).execute()
    
    # Add headers for Responded sheet
    responded_headers = [['Name', 'Email', 'Team', 'Date_Reached', 'Date_Responded', 'Response_Time_Hours', 'Form_Link']]
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range='Responded!A1:G1',
        valueInputOption='USER_ENTERED',
        body={'values': responded_headers}
    ).execute()
    
    print("Created tracking sheets:")
    print("- 'Reached Out': Shows everyone we contacted")
    print("- 'Responded': Shows who filled out the form")
    print("- 'Tracking': Original tracking (keeps both)")

def main():
    cfg = load_config()
    service = connect_to_sheets(cfg.google_creds_path)
    
    add_response_tracking(service, cfg.google_sheets_id)
    print("Done! Now you have better tracking.")

if __name__ == "__main__":
    main()
