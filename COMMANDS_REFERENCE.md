# 📋 COPY-PASTE SETUP COMMANDS

## Windows PowerShell Commands

### Step 1: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 2: Run Migrations
```powershell
python manage.py migrate
```

### Step 3: Create Superuser (if needed)
```powershell
python manage.py createsuperuser
```

### Step 4: Start Django Server
```powershell
python manage.py runserver
```

### Step 5: Verify Setup
```powershell
python verify_chatbot_setup.py
```

---

## Configuration: Edit .env File

### Option 1: Using PowerShell
```powershell
# Open with Notepad
notepad .env

# Copy and paste into the editor:
OPENAI_API_KEY=sk-your_actual_api_key_here
```

### Option 2: Using Command Prompt
```cmd
# Replace YOUR_KEY with your actual OpenAI API key
echo OPENAI_API_KEY=YOUR_KEY > .env
```

### Option 3: Using Python
```python
python setup_chatbot.py
# Interactive setup - will prompt for API key
```

---

## Linux/Mac Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver

# Verify setup
python verify_chatbot_setup.py
```

### Edit .env with nano
```bash
nano .env
# Then edit and save with Ctrl+O, Enter, Ctrl+X
```

### Edit .env with vim
```bash
vim .env
# Press 'i' to insert, then paste: OPENAI_API_KEY=sk-your_key
# Press Esc, then type :wq to save
```

---

## Getting Your OpenAI API Key

### Step 1: Go to OpenAI Website
```
https://platform.openai.com/api-keys
```

### Step 2: Create New Key
- Click "Create new secret key"
- Give it a name (e.g., "Farm-APP")
- Copy the key that appears

### Step 3: Key Format
Your key will look like:
```
sk-proj-...rest-of-key...
```

---

## One-Liner Setup (Windows PowerShell)

If you've already set your API key in the .env file:

```powershell
pip install -r requirements.txt; python manage.py migrate; python manage.py runserver
```

---

## Quick Test Commands

### Check Python Version
```bash
python --version
```
Expected: Python 3.8 or higher

### Check pip Packages
```bash
pip list | grep -E "openai|python-dotenv|Django"
```

### Check Django Setup
```bash
python manage.py check
```
Expected: System check identified no issues (0 silenced).

### Show Available URLs
```bash
python manage.py show_urls | findstr chat
```

### Check Database
```bash
python manage.py dbshell
.tables
```

---

## Troubleshooting Commands

### Reset Database
```bash
# WARNING: This deletes all data!
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Check Environment Variables
```python
python
>>> import os
>>> from dotenv import load_dotenv
>>> load_dotenv()
>>> os.getenv('OPENAI_API_KEY')
'sk-...' # Should show your key
```

### Test OpenAI Connection
```python
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
# Should print a response
```

---

## Server Running on Different Port

If port 8000 is busy:

```bash
python manage.py runserver 8001
```

Then visit: http://localhost:8001/

---

## Run Tests (Optional)

```bash
# Run all tests
python manage.py test

# Run only farm_app tests
python manage.py test farm_app

# Run chatbot-specific tests
python manage.py test farm_app.tests_chatbot
```

---

## View Logs (Debugging)

### Show All Migrations
```bash
python manage.py showmigrations
```

### Show Migration Plan
```bash
python manage.py migrate --plan
```

### Show All URL Patterns
```bash
python manage.py show_urls
```

### Django Shell (Interactive)
```bash
python manage.py shell
>>> from farm_app.models import ChatMessage
>>> ChatMessage.objects.count()
# Shows number of chats
```

---

## Clean Up

### Remove Cache Files
```bash
# Windows
rmdir /s __pycache__
rmdir /s .pytest_cache

# Linux/Mac
find . -type d -name "__pycache__" -exec rm -r {} +
find . -type d -name ".pytest_cache" -exec rm -r {} +
```

### Remove Old Migrations
```bash
# DON'T DO THIS unless you know what you're doing!
# Just leave migrations as they are
```

---

## Performance Tips

### Collect Static Files (Production)
```bash
python manage.py collectstatic
```

### Compress Database
```bash
python manage.py dbshell
VACUUM;
.exit
```

### Check Database Size
```bash
ls -lh db.sqlite3
```

---

## Summary

| Task | Command |
|------|---------|
| Install packages | `pip install -r requirements.txt` |
| Run migrations | `python manage.py migrate` |
| Start server | `python manage.py runserver` |
| Verify setup | `python verify_chatbot_setup.py` |
| Interactive setup | `python setup_chatbot.py` |
| Django shell | `python manage.py shell` |
| Check system | `python manage.py check` |
| Show URLs | `python manage.py show_urls` |

---

## Common Errors & Fixes

### "Module not found: openai"
```bash
pip install openai==1.3.0
```

### "No module named 'dotenv'"
```bash
pip install python-dotenv==1.0.0
```

### "Database locked"
```bash
# Close Django server (Ctrl+C) and restart
python manage.py runserver
```

### "Port 8000 already in use"
```bash
# Use different port
python manage.py runserver 8001
```

### "Invalid API key"
```bash
# Check your API key at: https://platform.openai.com/api-keys
# Edit .env file with correct key
```

---

## Ready? Let's Go! 🚀

1. Copy API key from: https://platform.openai.com/api-keys
2. Edit `.env` file and add your key
3. Run: `pip install -r requirements.txt`
4. Run: `python manage.py migrate`
5. Run: `python manage.py runserver`
6. Open: http://localhost:8000/
7. Login and click 🤖 button
8. Start asking farming questions!

**Happy farming!** 🚜🤖
