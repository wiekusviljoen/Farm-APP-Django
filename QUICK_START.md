# AI Chatbot - Quick Start Guide

## ⚡ 5-Minute Setup

### Step 1: Install (1 minute)
```bash
pip install -r requirements.txt
```

### Step 2: Get API Key (2 minutes)
1. Go to: https://platform.openai.com/api-keys
2. Create account or sign in
3. Click "Create new secret key"
4. Copy the key (looks like: `sk-...`)

### Step 3: Set API Key (1 minute)
**Option A: Windows PowerShell**
```powershell
$env:OPENAI_API_KEY = "sk-your-key-here"
```

**Option B: Create .env file**
```
# Create file named .env in your project root
OPENAI_API_KEY=sk-your-key-here
```

**Option C: Windows Command Prompt**
```cmd
set OPENAI_API_KEY=sk-your-key-here
```

### Step 4: Migrate Database (1 minute)
```bash
python manage.py migrate
```

### Step 5: Start Django
```bash
python manage.py runserver
```

## 🚀 Using the Chatbot

### Global Chatbot
```
Visit: http://localhost:8000/chatbot/
Ask: "What should I feed my cows?"
```

### Farm-Specific Chatbot
```
1. Go to a farm
2. Click "Chat with Farm Advisor"
Or: http://localhost:8000/farm/1/chatbot/
```

## 💬 Example Questions

```
"What's the best feed for pregnant cows?"
"How do I prevent cattle diseases?"
"What breed of cattle is best for my area?"
"How much feed do I need daily?"
"When should I vaccinate my animals?"
"Is my feed cost reasonable?"
```

## ✅ How to Know It Works

1. ✓ You see the chatbot interface
2. ✓ You type a question
3. ✓ AI responds with advice
4. ✓ Conversation appears in history

## ❌ Troubleshooting

| Problem | Solution |
|---------|----------|
| "API key not configured" | Check Step 3 - restart Django after setting key |
| "ModuleNotFoundError: openai" | Run: `pip install openai==1.3.0` |
| "Authentication error" | Verify API key is correct (starts with `sk-`) |
| No response | Check internet connection, OpenAI status |

## 📚 Documentation

- **Full Setup**: See `CHATBOT_SETUP.md`
- **Implementation Details**: See `CHATBOT_IMPLEMENTATION.md`
- **Django Docs**: https://docs.djangoproject.com/
- **OpenAI Docs**: https://platform.openai.com/docs

## 💰 Important Notes

⚠️ **OpenAI API is NOT FREE**
- Each chat message costs money
- ~$0.0005 per 1000 tokens (very cheap, but it adds up)
- Set spending limits: https://platform.openai.com/account/billing/limits
- Monitor usage: https://platform.openai.com/usage

## 🎯 Key Features

✅ AI gives farming advice
✅ Considers your specific farm data
✅ Saves conversation history
✅ Works offline for viewing past chats
✅ Mobile-friendly interface
✅ No page refresh needed

## 📝 File Changes Summary

```
NEW FILES:
- farm_app/templates/farm_app/chatbot.html
- farm_app/migrations/0030_chatmessage.py
- CHATBOT_SETUP.md
- CHATBOT_IMPLEMENTATION.md
- QUICK_START.md (this file)

MODIFIED FILES:
- requirements.txt (added openai, python-dotenv)
- farm_app/models.py (added ChatMessage)
- farm_app/forms.py (added ChatMessageForm)
- farm_app/views.py (added chatbot views)
- farm_app/urls.py (added chatbot URLs)
- farm_project/settings.py (added API config)
```

## 🔗 New URLs

```
/chatbot/                    - Global chatbot
/chat/                       - Send message (global)
/farm/<id>/chatbot/          - Farm-specific chatbot
/farm/<id>/chat/             - Send message (farm)
```

## 🎓 Next Steps

1. ✅ Complete the 5-minute setup above
2. ✅ Test with a simple question
3. ✅ Create a farm and use farm-specific chatbot
4. ✅ Try the example questions above
5. ✅ Customize AI behavior if desired (see CHATBOT_SETUP.md)

---

**Questions?** Check the full documentation in `CHATBOT_SETUP.md` 📖

**Ready to chat?** Go to `http://localhost:8000/chatbot/` 🚀
