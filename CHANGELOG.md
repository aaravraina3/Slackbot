# Generate Feedback Bot - Changelog

## Current Status: WORKING ✅
- Bot can send DMs successfully
- Google Sheets integration working
- Message templates updated
- Tracking sheets created

## Issues & Solutions

### 1. Email Lookup Problems ❌
**Issue:** Some people can't be found in Slack by email
- Neha Jha (jha.ne@northeastern.edu) - not found
- Some people might use different emails in Slack vs roster

**Solutions Needed:**
- [ ] Add fallback email lookup (try both Northeastern + personal)
- [ ] Add manual Slack username mapping
- [ ] Create error handling for missing users
- [ ] Add logging for failed lookups

### 2. Reaction Tracking Not Working ❌
**Issue:** Bot can't track reactions to messages
**Current Status:** Need additional Slack scopes

**Required Scopes:**
- `reactions:read` - Read reactions on messages
- `channels:history` - Read message history  
- `im:history` - Read DM history

**Alternative Solutions:**
- [ ] Ask people to reply "DONE" instead of react
- [ ] Check Google Form responses directly
- [ ] Use keyword detection in replies

### 3. Form Preview Not Showing ❌
**Issue:** Google Form not showing as embedded preview in Slack
**Status:** Partially fixed - URL on separate line
**Still needs:** Verification that previews work consistently

### 4. Message Template Updates ✅
**Changes Made:**
- Changed "team" to "Community team" 
- Updated cooldown from "4 weeks" to "until your whole team has done it"
- Added "React to this message after you're done so the bot can check you off"

## Technical Issues Fixed ✅

### SSL Certificate Error
**Problem:** `SSL: CERTIFICATE_VERIFY_FAILED`
**Solution:** Added SSL context that disables certificate verification

### Google Sheets Permissions
**Problem:** `HttpError 403` - Permission denied
**Solution:** Shared sheet with service account as Editor

### Missing Sheets
**Problem:** `HttpError 400` - Unable to parse range
**Solution:** Created missing "Roster", "Tracking", "Reached Out", "Responded" sheets

### Module Import Errors
**Problem:** `ModuleNotFoundError: No module named 'bot'`
**Solution:** Used `python -m scripts.script_name` and proper PYTHONPATH

## Next Steps

### High Priority
1. **Fix email lookup** - Add fallback mechanisms
2. **Implement reaction tracking** - Add required scopes or alternative method
3. **Test with more people** - Verify bot works with different users

### Medium Priority  
1. **Add error logging** - Track failed lookups and sends
2. **Create admin dashboard** - View who was contacted and who responded
3. **Add retry logic** - Handle temporary failures

### Low Priority
1. **Optimize message formatting** - Ensure consistent form previews
2. **Add analytics** - Track response rates by team
3. **Create backup systems** - Handle API failures gracefully

## Files Created/Modified

### Core Bot Files
- `bot/config.py` - Configuration and environment variables
- `bot/sheets.py` - Google Sheets integration
- `bot/slack.py` - Slack API integration (SSL fix)
- `bot/selection.py` - Random selection logic
- `bot/messages.py` - Message templates (updated)

### Scripts
- `scripts/run_selection.py` - Main selection script
- `scripts/send_reminders.py` - Reminder script
- `scripts/test_dry_run.py` - Testing script

### Tracking Sheets
- `create_tracking_sheet.py` - Creates Tracking sheet
- `add_response_tracking.py` - Creates Reached Out/Responded sheets
- `upload_roster_to_sheet.py` - Uploads roster data

### Test Files
- `test_message_aarav.py` - Test message to Aarav
- `test_message_neha.py` - Test message to Neha (failed)

## Environment Setup
- Virtual environment: `venv/`
- Dependencies: `requirements.txt`
- Environment variables: `.env`
- Google credentials: `credentials.json`

## Current Working Commands
```bash
# Test selection (no DMs sent)
python3 -m scripts.test_dry_run

# Send actual DMs
python3 -m scripts.run_selection

# Send reminders
python3 -m scripts.send_reminders
```

---
*Last Updated: $(date)*
