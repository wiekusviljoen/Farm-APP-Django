#!/usr/bin/env python
"""
Chatbot Setup Verification Script
Verifies all components are properly installed and configured
"""

import os
import sys
from pathlib import Path

def check_env_file():
    """Check if .env file exists and has OPENAI_API_KEY"""
    print("\n📋 Checking .env file...")
    env_path = Path(".env")
    
    if not env_path.exists():
        print("   ❌ .env file not found!")
        print("   📝 Creating .env file...")
        env_path.write_text("OPENAI_API_KEY=your_openai_api_key_here\n")
        print("   ✅ .env file created! Please add your OpenAI API key.")
        return False
    
    content = env_path.read_text()
    if "OPENAI_API_KEY" not in content:
        print("   ❌ OPENAI_API_KEY not found in .env")
        return False
    
    if "your_openai_api_key_here" in content:
        print("   ⚠️  OPENAI_API_KEY is not configured (still has placeholder)")
        print("   📝 Please replace 'your_openai_api_key_here' with your actual key")
        return False
    
    print("   ✅ .env file exists with OPENAI_API_KEY configured")
    return True

def check_dependencies():
    """Check if required packages are installed"""
    print("\n📦 Checking dependencies...")
    required = ['django', 'openai', 'dotenv']
    missing = []
    
    for package in required:
        try:
            __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - NOT INSTALLED")
            missing.append(package)
    
    if missing:
        print(f"\n   Run: pip install {' '.join(missing)}")
        return False
    return True

def check_database_migrations():
    """Check if migrations are applied"""
    print("\n🗄️  Checking database migrations...")
    try:
        import django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'farm_project.settings')
        django.setup()
        
        from django.db import connection
        from farm_app.models import ChatMessage
        
        # Check if ChatMessage table exists
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='farm_app_chatmessage';")
            result = cursor.fetchone()
            if result:
                print("   ✅ ChatMessage table exists in database")
                return True
            else:
                print("   ❌ ChatMessage table not found!")
                print("   📝 Run: python manage.py migrate")
                return False
    except Exception as e:
        print(f"   ❌ Error checking database: {e}")
        print("   📝 Run: python manage.py migrate")
        return False

def check_templates():
    """Check if template files exist"""
    print("\n📄 Checking template files...")
    templates = [
        "farm_app/templates/farm_app/chatbot.html",
        "farm_app/templates/farm_app/farm_list.html",
        "farm_app/templates/farm_app/farm_detail.html",
    ]
    
    all_exist = True
    for template in templates:
        if Path(template).exists():
            print(f"   ✅ {template}")
        else:
            print(f"   ❌ {template} - NOT FOUND")
            all_exist = False
    
    return all_exist

def check_views():
    """Check if chatbot views are defined"""
    print("\n🔍 Checking view functions...")
    try:
        from farm_app.views import farm_chatbot, send_chat_message, _build_farm_context
        print("   ✅ farm_chatbot view")
        print("   ✅ send_chat_message view")
        print("   ✅ _build_farm_context helper")
        return True
    except ImportError as e:
        print(f"   ❌ Missing view functions: {e}")
        return False

def check_urls():
    """Check if chatbot URLs are configured"""
    print("\n🌐 Checking URL configuration...")
    try:
        from farm_app.urls import urlpatterns
        chatbot_urls = [p.name for p in urlpatterns if 'chat' in p.name]
        expected = ['farm_chatbot', 'send_chat_message', 'chatbot', 'send_chat_message_global']
        
        for url in expected:
            if url in chatbot_urls:
                print(f"   ✅ {url} route")
            else:
                print(f"   ⚠️  {url} route not found")
        
        return len(chatbot_urls) >= 4
    except Exception as e:
        print(f"   ❌ Error checking URLs: {e}")
        return False

def main():
    """Run all checks"""
    print("=" * 50)
    print("🤖 FARM CHATBOT SETUP VERIFICATION")
    print("=" * 50)
    
    checks = [
        ("Environment File", check_env_file),
        ("Dependencies", check_dependencies),
        ("Templates", check_templates),
        ("Views", check_views),
        ("URLs", check_urls),
        ("Database", check_database_migrations),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"   ⚠️  Error during {name} check: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\n{passed}/{total} checks passed")
    
    if passed == total:
        print("\n✅ All checks passed! Your chatbot is ready to use!")
        print("\nNext steps:")
        print("1. Run: python manage.py runserver")
        print("2. Login to http://localhost:8000/")
        print("3. Click 'Chat with AI' button on the farm list")
        print("4. Start asking farming questions!")
        return 0
    else:
        print("\n⚠️  Some checks failed. Please review the errors above.")
        print("\nCommon fixes:")
        print("- Run: pip install -r requirements.txt")
        print("- Run: python manage.py migrate")
        print("- Add your OpenAI API key to .env")
        return 1

if __name__ == "__main__":
    sys.exit(main())
