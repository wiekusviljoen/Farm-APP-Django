# 🤖 Farm AI Chatbot - Complete Setup Guide

## Quick Start (5 minutes)

### Step 1: Get OpenAI API Key
1. Go to https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy the key (you'll only see it once!)

### Step 2: Configure Environment
The `.env` file is already created in your project root. Add your API key:

**File: `.env`**
```
OPENAI_API_KEY=sk-your_actual_key_here
```

Replace `sk-your_actual_key_here` with your actual OpenAI API key.

### Step 3: Run Migrations
```bash
python manage.py migrate
```

### Step 4: Run Django Server
```bash
python manage.py runserver
```

### Step 5: Access the Chatbot
1. Open http://localhost:8000/
2. Login with your farm account
3. Click **"🤖 Chat with AI"** button on any farm list or farm detail page
4. Start asking farming questions!

---

## Features

✅ **Farm-Specific Advice** - Click "Chat About This Farm" on any farm detail to get personalized advice  
✅ **Global Chatbot** - Click "Chat with AI" on farm list for general farming questions  
✅ **Chat History** - All conversations are saved and visible in the chatbot interface  
✅ **Real-time Responses** - AJAX-powered, no page reloads  
✅ **Secure** - HTML escaping protects against XSS attacks  

---

## What Can You Ask?

- 🌾 **Cattle Feeding**: "What should I feed my pregnant cows?"
- 🏥 **Disease Prevention**: "How do I prevent cattle diseases?"
- 👶 **Breeding**: "What breeds are best for Namibia?"
- 💰 **Cost Optimization**: "How can I reduce feed costs?"
- 📊 **Farm Management**: "Best practices for cattle management"
- ❓ **General Questions**: Anything about farming and animal care

---

## Technical Details

### What Was Added

**Database (1 migration)**
- `ChatMessage` model stores all conversations

**Backend (3 view functions)**
- `farm_chatbot()` - Display chatbot interface
- `send_chat_message()` - Process messages and call OpenAI
- `_build_farm_context()` - Extract farm data for AI context

**Frontend (1 template)**
- `chatbot.html` - Complete standalone chatbot UI with Bootstrap styling

**Configuration**
- `.env` file for API key storage
- `settings.py` updated to load `.env` with python-dotenv
- 4 URL routes for global and farm-specific chatbot access

### API Keys & Costs

**Getting Started (FREE)**
- OpenAI gives $5 free credits when you sign up
- Each chat message costs roughly $0.01

**Monitoring Usage**
- Visit: https://platform.openai.com/usage/overview
- Set up billing alerts to avoid surprises

---

## Troubleshooting

### "API key not configured"
**Solution**: 
1. Make sure `.env` file exists in project root
2. Check API key is correctly set: `OPENAI_API_KEY=sk-...`
3. Restart Django server: `python manage.py runserver`

### "Network error"
**Solution**:
1. Check internet connection
2. Verify OpenAI API is not down: https://status.openai.com/
3. Check Django console for detailed errors

### "Failed to get response"
**Solution**:
1. Verify API key is valid at https://platform.openai.com/api-keys
2. Check if OpenAI account has credits remaining
3. Look at Django console for specific error message

### Chatbot button not showing
**Solution**:
1. Make sure you're logged in
2. Try refreshing the page
3. Check if JavaScript is enabled in browser

---

## Environment Variables

The chatbot looks for `OPENAI_API_KEY` in this order:
1. `.env` file (loaded by `python-dotenv`)
2. System environment variables
3. `farm_project/settings.py` hardcoded value (⚠️ NOT RECOMMENDED)

**Best Practice**: Always use `.env` file

---

## Security Notes

✅ API keys are loaded from `.env` (never hardcoded)  
✅ HTML escaping prevents XSS attacks  
✅ Chat history is per-user (only you see your chats)  
✅ Farm-specific chats require ownership verification  
✅ All views require `@login_required` decorator  

---

## Next Steps

After setup is complete:
1. Test with a simple question
2. Customize the system prompt in `send_chat_message()` if needed
3. Monitor API usage at https://platform.openai.com/usage/overview
4. Add your farms and start getting AI-powered farming advice!

---

## Files Modified/Created

| File | Status | Changes |
|------|--------|---------|
| `.env` | ✅ Created | API key configuration |
| `requirements.txt` | ✅ Updated | Added openai & python-dotenv |
| `farm_app/models.py` | ✅ Updated | Added ChatMessage model |
| `farm_app/forms.py` | ✅ Updated | Added ChatMessageForm |
| `farm_app/views.py` | ✅ Updated | Added 3 chatbot functions |
| `farm_app/urls.py` | ✅ Updated | Added 4 chatbot routes |
| `farm_app/admin.py` | ✅ Updated | Added ChatMessageAdmin |
| `farm_app/templates/chatbot.html` | ✅ Created | Chatbot UI |
| `farm_project/settings.py` | ✅ Updated | dotenv + OPENAI_API_KEY |
| `farm_app/migrations/0030_chatmessage.py` | ✅ Created | Database table |

---

## Support

If you have issues:
1. Check the error message in Django console
2. Verify your OpenAI API key is valid
3. Make sure `.env` file exists and is readable
4. Try restarting `python manage.py runserver`

Enjoy your AI farming assistant! 🚜🤖
