# ✅ FARM AI CHATBOT - COMPLETE SETUP CHECKLIST

## Pre-Setup Requirements
- [ ] Python 3.8+ installed
- [ ] Django 6.0 installed
- [ ] Virtual environment activated (if using one)

## Installation Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```
**Check**:
```bash
pip list | grep -E "openai|python-dotenv"
```
Expected output:
- `openai` version 1.3.0+
- `python-dotenv` version 1.0.0+

### Step 2: Get OpenAI API Key
- [ ] Visit https://platform.openai.com/api-keys
- [ ] Click "Create new secret key"
- [ ] Copy the key (format: `sk-...`)
- [ ] Store it safely (you'll only see it once!)

### Step 3: Configure Environment
- [ ] Open `.env` file in project root
- [ ] Replace `your_openai_api_key_here` with your actual key
- [ ] Verify file looks like:
  ```
  OPENAI_API_KEY=sk-your_actual_key_123abc...
  ```
- [ ] Save the file

### Step 4: Run Database Migrations
```bash
python manage.py migrate
```
Expected output:
```
Applying farm_app.0030_chatmessage... OK
```

### Step 5: Create Superuser (if not done)
```bash
python manage.py createsuperuser
```

### Step 6: Start Django Server
```bash
python manage.py runserver
```
Expected output:
```
Starting development server at http://127.0.0.1:8000/
```

## Verification Steps

### Verify Dependencies
```bash
python -c "import openai; from dotenv import load_dotenv; print('✅ All packages installed')"
```

### Verify Environment Configuration
```bash
python -c "from dotenv import load_dotenv; import os; load_dotenv(); api_key=os.getenv('OPENAI_API_KEY'); print(f'✅ API Key: {api_key[:10]}...')"
```

### Verify Database
```bash
python manage.py shell
>>> from farm_app.models import ChatMessage
>>> print("✅ ChatMessage model accessible")
>>> exit()
```

### Verify Templates
- [ ] Check file exists: `farm_app/templates/farm_app/chatbot.html`
- [ ] Check file exists: `farm_app/templates/farm_app/farm_list.html`
- [ ] Check file exists: `farm_app/templates/farm_app/farm_detail.html`

### Verify Views
```bash
python -c "from farm_app.views import farm_chatbot, send_chat_message; print('✅ View functions available')"
```

### Verify URLs
```bash
python manage.py show_urls | grep chat
```
Expected output includes:
- `farm_app:farm_chatbot`
- `farm_app:send_chat_message`
- `farm_app:chatbot`
- `farm_app:send_chat_message_global`

## Browser Testing

### Test 1: Access Global Chatbot
1. [ ] Open http://127.0.0.1:8000/
2. [ ] Login with your farm account
3. [ ] Click "🤖 Chat with AI" button on farm list
4. [ ] Verify chatbot page loads
5. [ ] Check page shows "Farm Advisor AI" title
6. [ ] Check chat input box is visible

### Test 2: Test Farm-Specific Chatbot
1. [ ] Click on any farm
2. [ ] Click "🤖 Chat About This Farm" button
3. [ ] Verify page shows farm name in title
4. [ ] Verify chat history loads

### Test 3: Send Test Message
1. [ ] Type: "What should I feed my cattle?"
2. [ ] Click "Send Message"
3. [ ] Verify loading spinner appears
4. [ ] Verify AI response appears within 10 seconds
5. [ ] Verify message is saved to history

### Test 4: Check Chat Persistence
1. [ ] Refresh the page
2. [ ] Verify previous messages still visible
3. [ ] Type another message
4. [ ] Verify it appends to conversation

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| "API key not configured" | Check `.env` file has correct key format `sk-...` |
| "Network error" | Check internet connection, OpenAI API status |
| "No matching ChatMessage model" | Run `python manage.py migrate` |
| "Chatbot button not visible" | Clear browser cache, refresh page |
| "500 Error when sending message" | Check Django console for detailed error |
| "Template not found" | Verify chatbot.html exists in correct directory |

## Files Checklist

### Created Files
- [ ] `.env` - Contains OPENAI_API_KEY
- [ ] `CHATBOT_SETUP_FINAL.md` - Setup guide
- [ ] `verify_chatbot_setup.py` - Verification script
- [ ] `farm_app/migrations/0030_chatmessage.py` - Database migration

### Modified Files
- [ ] `requirements.txt` - Added openai, python-dotenv
- [ ] `farm_project/settings.py` - Added dotenv loading + OPENAI_API_KEY
- [ ] `farm_app/models.py` - Added ChatMessage model
- [ ] `farm_app/forms.py` - Added ChatMessageForm
- [ ] `farm_app/views.py` - Added 3 chatbot functions
- [ ] `farm_app/urls.py` - Added 4 chatbot routes
- [ ] `farm_app/admin.py` - Added ChatMessageAdmin
- [ ] `farm_app/templates/farm_app/chatbot.html` - Created chatbot UI
- [ ] `farm_app/templates/farm_app/farm_list.html` - Added chat button
- [ ] `farm_app/templates/farm_app/farm_detail.html` - Added chat button

## Performance & Monitoring

### Monitor API Usage
- Visit: https://platform.openai.com/usage/overview
- Set up billing alerts: https://platform.openai.com/account/billing/overview

### Expected Response Times
- First message: 2-5 seconds (API initialization)
- Subsequent messages: 1-3 seconds

### Cost Estimates
- Each message: ~$0.001-0.005 (very cheap)
- 100 messages: ~$0.10-0.50
- Monitor at: https://platform.openai.com/account/usage

## Security Checklist

- [ ] `.env` file NOT committed to git
- [ ] API key only accessible via environment variables
- [ ] Django DEBUG = False in production
- [ ] CSRF protection enabled (default)
- [ ] HTML escaping enabled (built-in)
- [ ] User authentication required (@login_required)
- [ ] Farm ownership validated for farm-specific chats

## Troubleshooting Commands

### Reset Everything
```bash
# Remove database
rm db.sqlite3

# Run migrations fresh
python manage.py migrate

# Create superuser again
python manage.py createsuperuser

# Restart server
python manage.py runserver
```

### View Logs
```bash
# View migrations
python manage.py showmigrations

# Check pending migrations
python manage.py migrate --plan

# View all URL patterns
python manage.py show_urls
```

### Test API Connection
```bash
python
>>> from openai import OpenAI
>>> import os
>>> from dotenv import load_dotenv
>>> load_dotenv()
>>> api_key = os.getenv('OPENAI_API_KEY')
>>> client = OpenAI(api_key=api_key)
>>> response = client.chat.completions.create(
...     model="gpt-3.5-turbo",
...     messages=[{"role": "user", "content": "Hello"}],
...     max_tokens=10
... )
>>> print(response.choices[0].message.content)
```

## Final Sign-Off

After completing all steps:

- [ ] All dependencies installed
- [ ] .env file configured with API key
- [ ] Database migrations applied
- [ ] Server running without errors
- [ ] Login working
- [ ] Chatbot buttons visible on farm pages
- [ ] Test message sent successfully
- [ ] AI response received
- [ ] Chat history persists after refresh

✅ **Your Farm AI Chatbot is ready to use!** 🤖🚜

For issues, check:
1. Django console for error messages
2. Browser console (F12) for JavaScript errors
3. https://platform.openai.com/usage/overview for API status
4. Run: `python verify_chatbot_setup.py`
