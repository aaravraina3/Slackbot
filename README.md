# Generate BSCI Slackbot 🤖

A beginner-friendly Slackbot for the Generate BSCI club. This bot helps automate common tasks and interactions in your Slack workspace.

## 🚀 Quick Start

### 1. Setup
```bash
# Clone the repository
git clone <your-repo-url>
cd Slackbot

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
```

### 2. Configure Environment
Edit `.env` file with your Slack app credentials:
```bash
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_APP_TOKEN=xapp-your-app-token
SIGNING_SECRET=your-signing-secret
```

### 3. Run the Bot
```bash
python main.py
```

## 📁 Project Structure

```
Slackbot/
├── README.md              # This file - start here!
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── main.py               # Main bot file - run this to start the bot
├── config/
│   ├── __init__.py
│   └── settings.py       # Bot configuration settings
├── handlers/
│   ├── __init__.py
│   ├── message_handler.py    # Handle incoming messages
│   ├── command_handler.py    # Handle slash commands
│   └── event_handler.py      # Handle Slack events
├── utils/
│   ├── __init__.py
│   ├── helpers.py        # Helper functions
│   └── database.py       # Database operations (if needed)
├── commands/
│   ├── __init__.py
│   ├── greeting.py       # Example: /hello command
│   ├── info.py          # Example: /info command
│   └── help.py          # Help command
└── tests/
    ├── __init__.py
    └── test_basic.py     # Basic tests
```

## 🛠️ For New Team Members

### Getting Started
1. **Read this README** - It explains everything you need to know
2. **Check out `main.py`** - This is where the bot starts
3. **Look at `handlers/`** - This is where message processing happens
4. **Explore `commands/`** - This is where you add new bot commands

### Adding New Commands
1. **Create a new file** in `commands/` folder
2. **Follow the pattern** in existing command files
3. **Register your command** in `handlers/command_handler.py`
4. **Test your command** locally

### Common Tasks
- **Add a new slash command**: See `commands/greeting.py` for example
- **Respond to messages**: See `handlers/message_handler.py`
- **Handle events**: See `handlers/event_handler.py`

## 🔧 Configuration

### Bot Permissions Needed
- `chat:write` - Send messages
- `commands` - Handle slash commands
- `channels:read` - Read channel information
- `users:read` - Read user information

### Environment Variables
- `SLACK_BOT_TOKEN` - Your bot's token (starts with xoxb-)
- `SLACK_APP_TOKEN` - Your app's token (starts with xapp-)
- `SIGNING_SECRET` - Used to verify requests from Slack

## 📝 Development Guidelines

### Code Style
- **Use clear variable names** (e.g., `user_message` not `msg`)
- **Add comments** explaining what your code does
- **Follow the existing patterns** in the codebase
- **Test your changes** before pushing

### Best Practices
- **Always handle errors** - Use try/except blocks
- **Log important events** - Use the logging system
- **Keep functions small** - One function, one job
- **Ask questions** - Better to ask than break things!

## 🐛 Troubleshooting

### Common Issues
1. **Bot not responding**: Check your tokens in `.env`
2. **Permission errors**: Verify bot has correct permissions
3. **Import errors**: Make sure you installed requirements.txt

### Getting Help
1. **Check the logs** - Look for error messages
2. **Read the code comments** - They explain what's happening
3. **Ask team members** - We're here to help!

## 🚀 Deployment

### Local Development
```bash
python main.py
```

### Production
- Use a process manager like PM2 or systemd
- Set up proper logging
- Monitor bot health

## 📚 Resources

- [Slack API Documentation](https://api.slack.com/)
- [Python Slack SDK](https://slack.dev/python-slack-sdk/)
- [Slack Bot Best Practices](https://api.slack.com/authentication/best-practices)

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Test thoroughly**
5. **Submit a pull request**

## 📞 Support

If you need help:
1. Check this README first
2. Look at existing code for examples
3. Ask team members for help
4. Create an issue in the repository

---

**Happy coding! 🎉**
