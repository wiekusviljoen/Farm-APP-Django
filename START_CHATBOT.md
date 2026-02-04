# 🎯 QUICK START - Farm AI Chatbot

## What You Need (3 steps, 5 minutes)

### 1️⃣ Get API Key
Go to: https://platform.openai.com/api-keys
- Click "Create new secret key"
- Copy it (looks like: `sk-...`)

### 2️⃣ Add to .env File
Edit `.env` in your project folder:
```
OPENAI_API_KEY=sk-paste_your_key_here
```

### 3️⃣ Run Commands
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## 🚀 You're Done!

Open http://localhost:8000/ and click **"🤖 Chat with AI"**

---

## What Works Now

✅ Click "Chat with AI" on farm list for general farming advice  
✅ Click "Chat About This Farm" on any farm for personalized tips  
✅ Get responses about cattle feeding, health, breeding, costs, etc.  
✅ Chat history is saved automatically  
✅ No page reloads - smooth AJAX responses  

---

## Questions?

**"API key not configured?"**  
→ Make sure `.env` file has your real key (not placeholder)

**"No responses from AI?"**  
→ Check you have OpenAI credits at https://platform.openai.com/account/billing

**"Still broken?"**  
→ Run: `python verify_chatbot_setup.py`

---

## Learn More

- Full setup guide: `CHATBOT_SETUP_FINAL.md`
- Complete checklist: `COMPLETE_SETUP_CHECKLIST.md`
- Verification script: `python verify_chatbot_setup.py`

**Enjoy your AI farming assistant!** 🚜🤖
