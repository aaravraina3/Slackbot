# API Gateway Setup for Slack Events

## Step 1: Create API Gateway

1. Go to **API Gateway** in AWS Console
2. Click **"Create API"**
3. Choose **"REST API"** → **"Build"**
4. Name: `generate-feedback-bot-api`
5. Description: `API for receiving Slack events`
6. Click **"Create API"**

## Step 2: Create Resource and Method

1. Click **"Actions"** → **"Create Resource"**
2. Resource Name: `slack-events`
3. Resource Path: `slack-events`
4. Enable CORS: **Yes**
5. Click **"Create Resource"**

6. Select the `slack-events` resource
7. Click **"Actions"** → **"Create Method"**
8. Choose **"POST"**
9. Click the checkmark

## Step 3: Configure Method

1. Integration type: **Lambda Function**
2. Use Lambda Proxy integration: **✅ Checked**
3. Lambda Region: `us-east-1` (or your region)
4. Lambda Function: `generate-feedback-bot`
5. Click **"Save"**
6. Click **"OK"** to give API Gateway permission

## Step 4: Deploy API

1. Click **"Actions"** → **"Deploy API"**
2. Deployment stage: **`prod`**
3. Click **"Deploy"**

## Step 5: Get the Endpoint URL

After deployment, you'll get a URL like:
```
https://abc123.execute-api.us-east-1.amazonaws.com/prod/slack-events
```

**Copy this URL!** You'll need it for Slack app configuration.

## Step 6: Configure Slack App

1. Go to your Slack app settings: https://api.slack.com/apps
2. Go to **"Event Subscriptions"**
3. Enable Events: **On**
4. Request URL: Paste your API Gateway URL
5. Slack will verify the URL (should show ✅)
6. Subscribe to Bot Events:
   - `reaction_added` ✅
   - `message.im` ✅ (optional)
7. Click **"Save Changes"**

## Step 7: Test the Integration

1. Send a test message from your bot
2. React to it with 👍
3. Check CloudWatch logs to see if the event was received

## Troubleshooting

### URL Verification Fails
- Make sure your Lambda function is deployed
- Check that the API Gateway is deployed to `prod`
- Verify the handler function name is correct

### Events Not Received
- Check CloudWatch logs for errors
- Verify Slack app has correct scopes
- Make sure the endpoint URL is correct

### Lambda Errors
- Check that environment variables are set
- Verify the bot module is in the deployment package
- Check that Google Sheets credentials are included
