# AI Chatbot Testing Guide

## Pre-Testing Checklist

Before testing, ensure:

- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] API key configured in environment
- [ ] Database migrated: `python manage.py migrate`
- [ ] Django server running: `python manage.py runserver`
- [ ] You have an active user account
- [ ] You have created at least one farm (for farm-specific testing)

---

## Test Scenario 1: Global Chatbot Access

### Steps

1. Log in to the application
2. Navigate to `http://localhost:8000/chatbot/`
3. Verify the chatbot interface loads

### Expected Results

✅ Page displays with:
- Header: "Farm Advisor AI"
- Chatbox with welcome message
- Text input field with label
- "Send Message" button
- Link to farms list

### Test Data

- Should show empty chat history on first visit

---

## Test Scenario 2: Farm-Specific Chatbot Access

### Steps

1. Navigate to farm list (`/`)
2. Click on any farm
3. Look for "Chat with Farm Advisor" button
4. Or manually visit: `/farm/1/chatbot/`

### Expected Results

✅ Chatbot loads with:
- Farm name displayed in header
- Same interface as global chatbot
- Empty chat history on first visit
- Navigation back to farm

### Test Data

- Should show farm location, breed, cattle counts in sidebar (if added to template)

---

## Test Scenario 3: Sending a Chat Message

### Steps

1. Navigate to global chatbot: `/chatbot/`
2. Type a question: "What should I feed my cows?"
3. Click "Send Message"
4. Wait for response

### Expected Results

✅ Message handling:
- Input field clears
- "Sending..." appears while waiting
- User message appears in chat history
- AI response appears below with lightbulb icon
- Chatbox auto-scrolls to latest message
- Button re-enables after response

### Example Questions to Test

```
"What should I feed my cows?"
"How do I prevent cattle diseases?"
"What is a good breed for dairy farming?"
"How much feed do I need for 50 cattle?"
"What's the best vaccination schedule?"
```

### Expected AI Responses

- Should contain relevant farming advice
- 100-500 words typically
- Formatted clearly
- Practical and actionable

---

## Test Scenario 4: Conversation History

### Steps

1. Send 3-5 messages to the chatbot
2. Refresh the page
3. Go to a different page and back
4. Check admin panel

### Expected Results

✅ Conversation persistence:
- Messages still visible after refresh
- Correct order (newest at bottom)
- Timestamps visible
- Proper user/AI attribution
- Admin shows conversations

---

## Test Scenario 5: Farm-Specific Context

### Steps

1. Create a farm with specific data:
   - Name: "Test Farm"
   - Location: "Windhoek"
   - Breed: "Bonsmara"
   - Cows: 25
   - Bulls: 5
   - Feed: "Energie Lek"

2. Chat about this farm
3. Ask: "What feed should I use for my cattle?"

### Expected Results

✅ Context awareness:
- AI mentions farm name
- References specific cattle counts
- Considers breed in recommendations
- Mentions current feed type
- Gives farm-specific advice

### Test Data

```python
# Create test farm
farm = Farm.objects.create(
    owner=user,
    name="Test Farm",
    location="Windhoek",
    breed="Bonsmara",
    cows_count=25,
    bulls_count=5,
    Feed="Energie Lek"
)
```

---

## Test Scenario 6: Error Handling

### Missing API Key

**Steps:**
1. Remove or blank `OPENAI_API_KEY` from environment
2. Try to send a message
3. Check response

**Expected Results:**
✅ User-friendly error message appears
- Says API key is not configured
- Suggests setting OPENAI_API_KEY

### Network Error

**Steps:**
1. Disconnect internet
2. Try to send a message

**Expected Results:**
✅ Graceful error handling:
- Message appears: "Network error"
- Suggests trying again
- No server errors in console

### Invalid API Key

**Steps:**
1. Set invalid API key: `set OPENAI_API_KEY=invalid`
2. Send a message

**Expected Results:**
✅ Clear error message:
- "Authentication error" appears
- User can see the error
- No crash or 500 error

---

## Test Scenario 7: Multi-User Isolation

### Steps

1. Create two user accounts
2. User A: Create Farm A, chat, send messages
3. User B: Create Farm B, chat, send messages
4. User A: Check they only see their farm/chats
5. User B: Check they only see their farm/chats

### Expected Results

✅ Data isolation:
- User A cannot see User B's farms
- User A cannot see User B's chats
- Each user sees only their data
- Admin sees all (proper security)

---

## Test Scenario 8: Admin Panel

### Steps

1. Log in as admin
2. Visit `/admin/farm_app/chatmessage/`
3. Verify chat listing
4. Try filtering by user/farm
5. Try searching messages
6. View individual chat

### Expected Results

✅ Admin features:
- All chats visible
- Filter by user works
- Filter by farm works
- Filter by date works
- Search functionality works
- Message previews show
- Full messages readable
- No add/edit options
- Delete option works

---

## Test Scenario 9: Responsive Design

### Desktop Test

**Steps:**
1. Open chatbot on desktop browser
2. Verify layout and spacing
3. Send a message
4. Check response formatting

**Expected Results:**
✅ Desktop optimization:
- Centered layout
- Readable text size
- Good spacing
- Responsive buttons
- Scrollable chat area

### Mobile Test

**Steps:**
1. Open Chrome DevTools (F12)
2. Toggle device toolbar (mobile view)
3. Test at different breakpoints (375px, 768px)
4. Try sending messages on mobile

**Expected Results:**
✅ Mobile optimization:
- Readable on small screens
- Touch-friendly buttons
- Proper text wrapping
- Scrollable chat
- No horizontal scroll
- Full functionality works

---

## Test Scenario 10: Performance

### Load Testing

**Steps:**
1. Send 20 messages rapidly
2. Measure response time
3. Check for errors
4. Monitor database size

**Expected Results:**
✅ Performance metrics:
- Response time < 5 seconds
- No timeout errors
- No database corruption
- Consistent performance
- Memory usage reasonable

### Database Size

**Steps:**
```python
# In Django shell
python manage.py shell
from farm_app.models import ChatMessage
ChatMessage.objects.count()  # Should show number of messages
```

**Expected:**
- One row per user + AI message pair
- Growing incrementally with usage

---

## Manual Testing Checklist

### Functionality
- [ ] Global chatbot loads
- [ ] Farm-specific chatbot loads
- [ ] Messages send successfully
- [ ] AI responses appear
- [ ] Chat history persists
- [ ] Error messages show
- [ ] Admin panel works
- [ ] Logout clears session
- [ ] Login required enforced

### Data Integrity
- [ ] Chat timestamps accurate
- [ ] User attribution correct
- [ ] Farm association correct
- [ ] History ordered by date
- [ ] No duplicate messages
- [ ] No lost messages

### Security
- [ ] Can't access other user's chats
- [ ] Can't access other user's farms
- [ ] API key not exposed
- [ ] CSRF tokens working
- [ ] Login redirect works
- [ ] Admin protected

### UI/UX
- [ ] Interface is clean
- [ ] Buttons responsive
- [ ] Messages readable
- [ ] Timestamps visible
- [ ] Loading states clear
- [ ] Errors are helpful

---

## Automated Testing (Optional)

### Write Unit Tests

```python
# farm_app/tests.py
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Farm, ChatMessage

class ChatbotTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test', 'test@test.com', 'pass')
        self.farm = Farm.objects.create(owner=self.user, name='Test', location='Test')
        self.client = Client()
    
    def test_chatbot_requires_login(self):
        response = self.client.get('/chatbot/')
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_chatbot_loads_for_logged_in(self):
        self.client.login(username='test', password='pass')
        response = self.client.get('/chatbot/')
        self.assertEqual(response.status_code, 200)
    
    def test_farm_chatbot_access(self):
        self.client.login(username='test', password='pass')
        response = self.client.get(f'/farm/{self.farm.id}/chatbot/')
        self.assertEqual(response.status_code, 200)
```

### Run Tests

```bash
python manage.py test farm_app.tests.ChatbotTests
```

---

## Troubleshooting Tests

### Issue: "Page not found"
- Verify URLs are in `farm_app/urls.py`
- Check `url()` syntax

### Issue: "Import errors"
- Verify models imported correctly
- Check forms exist

### Issue: "Template not found"
- Verify `chatbot.html` exists in correct location
- Check template path

### Issue: "API key errors"
- Set `OPENAI_API_KEY` environment variable
- Restart Django server

---

## Test Results Template

```
Date: ___________
Tester: ___________

Scenario 1 (Global Access): PASS / FAIL
Scenario 2 (Farm Access): PASS / FAIL
Scenario 3 (Send Message): PASS / FAIL
Scenario 4 (History): PASS / FAIL
Scenario 5 (Context): PASS / FAIL
Scenario 6 (Errors): PASS / FAIL
Scenario 7 (Multi-user): PASS / FAIL
Scenario 8 (Admin): PASS / FAIL
Scenario 9 (Responsive): PASS / FAIL
Scenario 10 (Performance): PASS / FAIL

Issues Found:
1. ___________
2. ___________
3. ___________

Overall Status: READY FOR PRODUCTION / NEEDS FIXES
```

---

## Success Criteria

✅ All test scenarios pass
✅ No error messages without proper handling
✅ Data properly isolated between users
✅ Admin panel shows correct data
✅ Performance acceptable
✅ Mobile and desktop layouts work
✅ API integration functional

---

## Next Steps

1. ✅ Complete all test scenarios
2. ✅ Document any issues found
3. ✅ Fix identified bugs
4. ✅ Re-test affected areas
5. ✅ Mark as production-ready

**Status**: Ready for testing! 🧪
