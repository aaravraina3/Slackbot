# EventBridge Setup for Scheduling

## Step 1: Create EventBridge Rules

### Rule 1: Weekly Selection (Monday 9am EST)

1. Go to **EventBridge** in AWS Console
2. Click **"Create rule"**
3. Name: `generate-feedback-weekly-selection`
4. Description: `Run weekly selection every Monday at 9am EST`
5. Event pattern: **Schedule**
6. Cron expression: `0 14 * * MON *` (9am EST = 2pm UTC)
7. Click **"Next"**

8. Target type: **AWS service**
9. Service: **Lambda function**
10. Function: `generate-feedback-bot`
11. Click **"Next"**

12. Configure input: **Constant (JSON text)**
13. JSON input:
```json
{
  "action": "weekly_selection",
  "source": "aws.events"
}
```
14. Click **"Next"** → **"Create rule"**

### Rule 2: First Reminders (Wednesday 2pm EST)

1. Create another rule: `generate-feedback-first-reminders`
2. Cron expression: `0 19 * * WED *` (2pm EST = 7pm UTC)
3. JSON input:
```json
{
  "action": "send_first_reminders", 
  "source": "aws.events"
}
```

### Rule 3: Final Reminders (Friday 3pm EST)

1. Create another rule: `generate-feedback-final-reminders`
2. Cron expression: `0 20 * * FRI *` (3pm EST = 8pm UTC)
3. JSON input:
```json
{
  "action": "send_final_reminders",
  "source": "aws.events"
}
```

## Step 2: Update Lambda Function

The Lambda function needs to handle these scheduled events. Update `slack_events_handler.py`:

```python
def handle_scheduled_event(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """Handle scheduled events (weekly selection, reminders)"""
    action = event.get('action', '')
    
    if action == 'weekly_selection':
        # Run the weekly selection
        from scripts.run_selection import main as run_selection
        run_selection()
        
    elif action == 'send_first_reminders':
        # Send first reminders
        from scripts.send_reminders import main as send_reminders
        send_reminders()
        
    elif action == 'send_final_reminders':
        # Send final reminders
        from scripts.send_reminders import main as send_reminders
        send_reminders()
    
    return {
        'statusCode': 200,
        'body': json.dumps({'status': f'Completed {action}'})
    }
```

## Step 3: Test the Rules

1. Go to EventBridge → Rules
2. Click on a rule
3. Click **"Test rule"**
4. Send a test event to verify Lambda receives it

## Cron Expression Reference

```
# Format: minute hour day-of-month month day-of-week year
# All times are UTC

0 14 * * MON *    # Monday 9am EST (2pm UTC)
0 19 * * WED *    # Wednesday 2pm EST (7pm UTC)  
0 20 * * FRI *    # Friday 3pm EST (8pm UTC)
```

## Timezone Considerations

- **EST (Eastern Standard Time)**: UTC-5
- **EDT (Eastern Daylight Time)**: UTC-4
- **Adjust cron expressions** if you're in a different timezone

## Monitoring

- Check **CloudWatch Logs** for Lambda execution logs
- Check **EventBridge** → **Rules** for rule execution history
- Set up **CloudWatch Alarms** for failed executions

## Cost

- **EventBridge**: First 1M events/month are FREE
- **Lambda**: First 1M requests/month are FREE
- **Total cost**: $0/month for your use case!
