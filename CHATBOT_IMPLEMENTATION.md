# AI Chatbot Implementation Summary

## What Was Added

A complete AI-powered chatbot feature has been integrated into your Farm APP Django project. The chatbot provides expert advice on farming and animal feeds using OpenAI's GPT-3.5-turbo model.

## Files Created/Modified

### New Files
1. **farm_app/templates/farm_app/chatbot.html** - Chatbot UI with conversation interface
2. **farm_app/migrations/0030_chatmessage.py** - Database migration for ChatMessage model
3. **CHATBOT_SETUP.md** - Comprehensive setup and usage guide

### Modified Files
1. **requirements.txt** - Added `openai==1.3.0` and `python-dotenv==1.0.0`
2. **farm_app/models.py** - Added `ChatMessage` model for storing conversation history
3. **farm_app/forms.py** - Added `ChatMessageForm` for message input
4. **farm_app/views.py** - Added three new functions:
   - `farm_chatbot()` - Display chatbot interface
   - `send_chat_message()` - Handle message processing and AI response
   - `_build_farm_context()` - Build farm-specific context for AI
5. **farm_app/urls.py** - Added 4 new URL routes for chatbot functionality
6. **farm_project/settings.py** - Added OpenAI API key configuration

## New Features

### 1. Global Chatbot
- Access at `/chatbot/` URL
- Get general farming advice
- Considers all user's farms for context

### 2. Farm-Specific Chatbot
- Access via each farm's detail page
- Contextual advice based on specific farm data:
  - Breed type
  - Herd composition (cows, bulls, calves)
  - Pregnancy status
  - Illness count
  - Current feed type
  - Vaccination status
  - Location

### 3. Conversation Persistence
- All conversations saved to database
- View chat history anytime
- Referenced with timestamp and farm association

## New Database Table

**ChatMessage**
- Stores user questions and AI responses
- Links to user and optional farm
- Timestamps each interaction
- Ordered by recency

## Key Components

### Models
```python
class ChatMessage(models.Model):
    user = ForeignKey(User, on_delete=models.CASCADE)
    user_message = TextField()
    ai_response = TextField()
    created_at = DateTimeField(auto_now_add=True)
    farm = ForeignKey(Farm, null=True, blank=True)
```

### Views
- `farm_chatbot(request, farm_id=None)` - Display chatbot UI
- `send_chat_message(request, farm_id=None)` - Handle AJAX chat requests
- `_build_farm_context(user, farm=None)` - Create AI context

### URLs
- `chatbot/` - Global chatbot (GET)
- `chat/` - Send message (POST)
- `farm/<farm_id>/chatbot/` - Farm chatbot (GET)
- `farm/<farm_id>/chat/` - Farm message (POST)

## Configuration

### Required Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Get OpenAI API key from https://platform.openai.com/api-keys
3. Set environment variable:
   ```bash
   set OPENAI_API_KEY=sk-...
   ```
4. Run migrations: `python manage.py migrate`

### AI System Prompt
The AI is configured to:
- Act as agricultural consultant for cattle farming in Namibia
- Provide advice on:
  - Cattle feeding and nutrition
  - Farm management practices
  - Disease prevention
  - Breeding recommendations
  - Feed cost optimization
- Consider local (Namibia) conditions
- Use farmer's data for personalized advice

## Frontend Features

### Chatbot Interface
- **Message Input**: Textarea for questions
- **Chat Display**: Separate styling for user vs AI messages
- **Timestamps**: Shows when each message was sent
- **Auto-scroll**: Automatically scrolls to latest messages
- **AJAX Submission**: Messages sent without page reload
- **Responsive Design**: Works on mobile and desktop
- **Loading States**: Shows "Sending..." during request

### User Experience
- Bootstrap styling for clean appearance
- Clear visual distinction between user/AI messages
- Helpful examples for first-time users
- Easy navigation back to farms
- No page refresh needed

## API Integration

### OpenAI API
- Model: gpt-3.5-turbo
- Temperature: 0.7 (balanced creativity)
- Max tokens: 500 (response length limit)
- Timeout: Built-in error handling

### Configuration in Settings
```python
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', None)
```

## Security Features

✅ Login required for all chatbot features
✅ Users can only access their own farms
✅ API key stored in environment variables
✅ CSRF protection on forms
✅ No sensitive data logged

## Performance Considerations

- API calls handled asynchronously via AJAX
- Conversation history retrieved from database
- No page refresh needed
- Graceful error handling
- Timeout protection

## Testing

To test the chatbot:

1. **Create a farm** with animal/feed details
2. **Navigate to farm chatbot**: `/farm/<id>/chatbot/`
3. **Ask a question** like "What feed should I use for pregnant cows?"
4. **Verify response** appears from AI
5. **Check history** - should show conversation

Example questions:
- "What feed should I give my bulls?"
- "How do I prevent cattle diseases?"
- "What's the best breed for my area?"
- "How much feed do I need daily?"
- "When should I vaccinate my calves?"

## Error Handling

The chatbot includes error handling for:
- Missing API key → User-friendly message
- Network errors → Retry prompt
- Invalid input → Form validation
- API failures → Error notification
- Timeout → Connection error message

## Next Steps

1. **Install dependencies**: `pip install openai python-dotenv`
2. **Get API key**: Create account at OpenAI
3. **Configure environment**: Add `OPENAI_API_KEY` to .env
4. **Run migrations**: `python manage.py migrate`
5. **Test chatbot**: Create farm and start chatting!

See **CHATBOT_SETUP.md** for detailed setup instructions.

## Costs

⚠️ OpenAI API usage has associated costs:
- gpt-3.5-turbo: ~$0.0005 per 1K tokens
- Monitor usage at https://platform.openai.com/usage
- Set spending limits to prevent surprises

## Support Resources

- OpenAI Documentation: https://platform.openai.com/docs
- Setup Guide: CHATBOT_SETUP.md (in project root)
- Django Documentation: https://docs.djangoproject.com/
