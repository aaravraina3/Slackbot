# GCP Cloud Scheduler Setup for Generate Feedback Bot

## Step 1: Create Cloud Scheduler Jobs

### Job 1: Weekly Selection (Monday 9am EST)

1. **Go to Cloud Scheduler:** https://console.cloud.google.com/cloudscheduler
2. **Click "Create Job"**
3. **Configure:**
   - **Name:** `generate-feedback-weekly-selection`
   - **Description:** `Run weekly selection every Monday at 9am EST`
   - **Frequency:** `0 14 * * MON` (9am EST = 2pm UTC)
   - **Timezone:** `America/New_York`
   - **Target Type:** `HTTP`
   - **URL:** `https://YOUR_REGION-YOUR_PROJECT.cloudfunctions.net/generate-feedback-bot`
   - **HTTP Method:** `POST`
   - **Headers:** `Content-Type: application/json`
   - **Body:**
   ```json
   {
     "action": "weekly_selection"
   }
   ```
4. **Click "Create"**

### Job 2: First Reminders (Wednesday 2pm EST)

1. **Create another job:** `generate-feedback-first-reminders`
2. **Frequency:** `0 19 * * WED` (2pm EST = 7pm UTC)
3. **Body:**
   ```json
   {
     "action": "send_first_reminders"
   }
   ```

### Job 3: Final Reminders (Friday 3pm EST)

1. **Create another job:** `generate-feedback-final-reminders`
2. **Frequency:** `0 20 * * FRI` (3pm EST = 8pm UTC)
3. **Body:**
   ```json
   {
     "action": "send_final_reminders"
   }
   ```

### Job 4: Reaction Checking (Every Hour)

1. **Create another job:** `generate-feedback-check-reactions`
2. **Frequency:** `0 * * * *` (every hour)
3. **Body:**
   ```json
   {
     "action": "check_reactions"
   }
   ```

## Step 2: Test the Jobs

1. **Go to Cloud Scheduler**
2. **Click on a job**
3. **Click "Run Now"** to test
4. **Check Cloud Function logs** to see if it worked

## Cron Expression Reference

```
# Format: minute hour day-of-month month day-of-week
# All times are in the specified timezone

0 14 * * MON    # Monday 9am EST
0 19 * * WED    # Wednesday 2pm EST  
0 20 * * FRI    # Friday 3pm EST
0 * * * *       # Every hour
```

## Monitoring

- **Cloud Scheduler:** View job execution history
- **Cloud Functions:** View function logs
- **Cloud Monitoring:** Set up alerts for failures

## Cost

- **Cloud Functions:** 2M invocations/month FREE
- **Cloud Scheduler:** 3 jobs/month FREE
- **Total cost:** $0/month for your use case!

## Troubleshooting

### Job Fails
- Check Cloud Function logs
- Verify the function URL is correct
- Check environment variables are set

### Function Timeout
- Increase timeout in Cloud Function settings
- Check if Google Sheets API is responding

### Permission Issues
- Ensure Cloud Scheduler has permission to invoke Cloud Functions
- Check service account permissions
