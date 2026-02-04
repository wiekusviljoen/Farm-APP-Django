#!/usr/bin/env python3
"""
Farm AI Chatbot - Quick Setup Script
Run this to complete the final setup steps
"""

import os
import sys
from pathlib import Path

print("\n" + "="*60)
print("🤖 FARM AI CHATBOT - QUICK SETUP")
print("="*60)

# Step 1: Check .env file
print("\n📋 Step 1: Checking .env file...")
env_file = Path(".env")
if env_file.exists():
    content = env_file.read_text()
    if "your_openai_api_key_here" in content:
        print("   ⚠️  .env file exists but API key is not configured!")
        print("   📝 Please edit .env and replace 'your_openai_api_key_here'")
        print("      with your actual OpenAI API key (sk-...)")
        print("\n   Get API key from: https://platform.openai.com/api-keys")
        api_key = input("\n   Enter your OpenAI API key (or press Enter to skip): ").strip()
        if api_key:
            if api_key.startswith("sk-"):
                new_content = content.replace("your_openai_api_key_here", api_key)
                env_file.write_text(new_content)
                print("   ✅ .env file updated!")
            else:
                print("   ❌ Invalid API key format (should start with 'sk-')")
        else:
            print("   ℹ️  Skipped. Remember to add your API key to .env later!")
    else:
        print("   ✅ .env file is configured with API key!")
else:
    print("   ⚠️  .env file not found! Creating...")
    env_file.write_text("OPENAI_API_KEY=your_openai_api_key_here\n")
    print("   📝 Please edit .env and add your OpenAI API key")
    print("   Get API key from: https://platform.openai.com/api-keys")

# Step 2: Check requirements
print("\n📦 Step 2: Checking dependencies...")
try:
    import openai
    import dotenv
    print("   ✅ All required packages are installed!")
except ImportError:
    print("   ⚠️  Missing dependencies!")
    print("   Run: pip install -r requirements.txt")

# Step 3: Check database
print("\n🗄️  Step 3: Checking database...")
try:
    from django.core.management import execute_from_command_line
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'farm_project.settings')
    
    import django
    django.setup()
    
    from farm_app.models import ChatMessage
    from django.db import connection
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='farm_app_chatmessage';")
        if cursor.fetchone():
            print("   ✅ Database is ready (ChatMessage table exists)!")
        else:
            print("   ⚠️  Database not initialized!")
            print("   Run: python manage.py migrate")
except Exception as e:
    print(f"   ⚠️  Error checking database: {e}")
    print("   Run: python manage.py migrate")

# Step 4: Summary
print("\n" + "="*60)
print("✅ SETUP COMPLETE!")
print("="*60)

print("""
Next steps:

1. Make sure .env has your OpenAI API key:
   OPENAI_API_KEY=sk-your_actual_key_here

2. Start the Django server:
   python manage.py runserver

3. Open in browser:
   http://localhost:8000/

4. Login and click "🤖 Chat with AI" button

5. Start asking farming questions!

Documentation:
- START_CHATBOT.md - Quick start guide
- CHATBOT_SETUP_FINAL.md - Full setup guide
- COMPLETE_SETUP_CHECKLIST.md - Detailed checklist
- verify_chatbot_setup.py - Run verification

Enjoy! 🚜🤖
""")

print("="*60)
