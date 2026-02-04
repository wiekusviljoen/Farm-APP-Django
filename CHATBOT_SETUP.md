# Farm APP AI Chatbot Setup Guide

## Overview

The AI Chatbot feature has been successfully added to your Farm APP Django project. It provides expert farming and animal feed advice powered by OpenAI's GPT-3.5.

## Features

✅ **AI-Powered Chatbot**: Ask questions about:
- Cattle feeding and nutrition
- Farm management practices
- Disease prevention and animal health
- Breeding recommendations
- Feed cost optimization

✅ **Farm-Specific Context**: The chatbot considers your farm data when giving advice
✅ **Conversation History**: All conversations are saved and retrievable
✅ **Two Access Modes**:
- Global chatbot (accessible from main app)
- Farm-specific chatbot (provides advice tailored to specific farms)

## Installation Steps

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `openai==1.3.0` - OpenAI API client
- `python-dotenv==1.0.0` - Environment variable management

### 2. Get OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Sign in or create an OpenAI account
3. Generate a new API key
4. Keep it safe - you'll need it next

### 3. Configure Environment

Option A: Using .env file (Recommended)
```bash
# Create a .env file in the project root
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

Option B: Set environment variable directly
```bash
# Windows PowerShell
$env:OPENAI_API_KEY = "your_api_key_here"

# Windows CMD
set OPENAI_API_KEY=your_api_key_here

# Linux/Mac
export OPENAI_API_KEY="your_api_key_here"
```

Option C: Update settings.py directly (not recommended for production)
```python
# In farm_project/settings.py
OPENAI_API_KEY = 'your_api_key_here'
```

### 4. Run Database Migrations

```bash
python manage.py migrate
```

This creates the `ChatMessage` table to store conversation history.

### 5. Start Using the Chatbot

**Global Chatbot** (access from main app):
- Navigate to `/chatbot/` or look for chatbot link in the UI

**Farm-Specific Chatbot** (tailored to your farm):
- Go to any farm detail page
- Look for the "Chat with Farm Advisor" button/link
- Or navigate to `/farm/<farm_id>/chatbot/`

## Usage

1. **Ask Questions**: Type your farming question in the message box
2. **Get Advice**: The AI will respond with expert advice
3. **View History**: All previous conversations are displayed
4. **Context-Aware**: For farm-specific chats, the AI knows your farm details

## File Structure

New files/modifications:
```
farm_app/
├── models.py (added ChatMessage model)
├── forms.py (added ChatMessageForm)
├── views.py (added chatbot views)
├── urls.py (added chatbot URLs)
├── templates/farm_app/
│   └── chatbot.html (new)
└── migrations/
    └── 0030_chatmessage.py (new)

farm_project/
└── settings.py (added OPENAI_API_KEY config)

requirements.txt (added openai, python-dotenv)
```

## API Configuration

### Settings.py Configuration

The following settings are available in `farm_project/settings.py`:

```python
# OpenAI Configuration
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', None)
```

### URL Routes

**New URLs added:**
- `chatbot/` - Global chatbot interface
- `chat/` - Send message to global chatbot (POST)
- `farm/<farm_id>/chatbot/` - Farm-specific chatbot
- `farm/<farm_id>/chat/` - Send message to farm-specific chatbot (POST)

## Database Schema

### ChatMessage Model

```python
class ChatMessage(models.Model):
    user = ForeignKey(User)  # Who asked the question
    user_message = TextField()  # The question
    ai_response = TextField()  # The AI's response
    created_at = DateTimeField(auto_now_add=True)  # When conversation occurred
    farm = ForeignKey(Farm, null=True, blank=True)  # Associated farm (optional)
```

## Troubleshooting

### Issue: "OpenAI API key not configured"

**Solution**: 
1. Verify your API key is set correctly in .env or environment
2. Restart your Django development server
3. Check that `OPENAI_API_KEY` is in settings.py

### Issue: "ModuleNotFoundError: No module named 'openai'"

**Solution**: Run `pip install openai==1.3.0`

### Issue: "Authentication error from OpenAI"

**Solution**:
1. Verify your API key is correct
2. Check your OpenAI account has available credits
3. Ensure you're using the correct API key (not the org ID)

### Issue: Chatbot not responding / timeout

**Solution**:
1. Check your internet connection
2. Verify OpenAI API status at https://status.openai.com/
3. Try again - OpenAI may have temporary issues

## Customization

### Change AI Behavior

Edit the system prompt in `views.py` function `send_chat_message()`:

```python
system_prompt = f"""You are an expert agricultural consultant...
# Modify this prompt to customize the AI's behavior
```

### Change Model

Change the model in the API call (currently gpt-3.5-turbo):

```python
response = client.chat.completions.create(
    model="gpt-3.5-turbo",  # Change this
    ...
)
```

Available models:
- `gpt-3.5-turbo` (faster, cheaper)
- `gpt-4` (more powerful, more expensive)
- `gpt-4-turbo-preview` (latest GPT-4)

### Change Response Length

Modify the `max_tokens` parameter:

```python
response = client.chat.completions.create(
    ...
    max_tokens=500,  # Change this (1-4096)
)
```

### Change Temperature (Creativity)

Adjust creativity level (0-2):

```python
response = client.chat.completions.create(
    ...
    temperature=0.7,  # Change this (0=factual, 2=creative)
)
```

## Security Notes

⚠️ **Never commit your API key to version control!**

- Keep `OPENAI_API_KEY` in `.env` file
- Add `.env` to `.gitignore`
- Use environment variables in production
- Rotate your API key periodically
- Monitor API usage at https://platform.openai.com/usage

## Costs

OpenAI API calls are **not free**. Monitor your usage:

1. Visit https://platform.openai.com/usage
2. Set spending limits to prevent unexpected charges
3. gpt-3.5-turbo is the most affordable model
4. Each chat message incurs a small cost

## Support

For issues with the chatbot implementation, check:
- Django logs for errors
- OpenAI API documentation: https://platform.openai.com/docs
- This project's README.md

## Next Steps

1. ✅ Install requirements
2. ✅ Set up API key
3. ✅ Run migrations
4. ✅ Start chatting!

Enjoy your AI farming advisor! 🌾🤖
