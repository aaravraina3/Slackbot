#!/usr/bin/env python3
"""
Convert CSV data to Google Sheet format for the feedback bot
"""

import csv
import sys

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

def main():
    csv_file = 'Slackbot copy F25 Generate Onboarding Form (Responses) - Form responses 1.csv'
    
    print("Converting CSV to Roster format...")
    roster = convert_csv_to_roster(csv_file)
    
    print(f"Found {len(roster)} members")
    print("\nRoster data (Name, Email, Team, Status):")
    print("-" * 60)
    
    for member in roster:
        print(f"{member[0]:<25} | {member[1]:<30} | {member[2]:<15} | {member[3]}")
    
    print(f"\nTotal: {len(roster)} members")
    
    # Show team breakdown
    teams = {}
    for member in roster:
        team = member[2]
        teams[team] = teams.get(team, 0) + 1
    
    print("\nTeam breakdown:")
    for team, count in sorted(teams.items()):
        print(f"  {team}: {count} members")

if __name__ == "__main__":
    main()
