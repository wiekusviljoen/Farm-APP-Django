# AI Chatbot Integration Reference

## Integration Points

This document shows where the chatbot integrates with your existing Farm APP.

---

## Database Level

### ChatMessage Model

**Location**: `farm_app/models.py`

```python
class ChatMessage(models.Model):
    user = ForeignKey(User, on_delete=models.CASCADE)
    farm = ForeignKey(Farm, null=True, blank=True, on_delete=models.CASCADE)
    user_message = TextField()
    ai_response = TextField()
    created_at = DateTimeField(auto_now_add=True)
```

**Relationships**:
- Links to Django's built-in `User` model
- Optional link to your `Farm` model
- Stores full conversation text
- Auto-timestamps each message

---

## View Layer Integration

### Views Integration

**File**: `farm_app/views.py`

**New imports**:
```python
from .models import ChatMessage
from .forms import ChatMessageForm
from openai import OpenAI
```

**New functions**:

1. **farm_chatbot()**
   - Receives farm_id as optional parameter
   - Retrieves chat history for user/farm
   - Renders `chatbot.html` template
   - No changes to existing views

2. **send_chat_message()**
   - Handles AJAX POST requests
   - Validates form with `ChatMessageForm`
   - Calls OpenAI API
   - Saves to `ChatMessage` model
   - Returns JSON response
   - No changes to existing views

3. **_build_farm_context()**
   - Helper function for AI context
   - Queries `Farm` model for context data
   - Used by `send_chat_message()`

**Existing views**: No changes to any existing views

---

## URL Configuration

### New Routes

**File**: `farm_app/urls.py`

```python
# Global chatbot routes
path('chatbot/', views.farm_chatbot, name='chatbot'),
path('chat/', views.send_chat_message, name='send_chat_message_global'),

# Farm-specific chatbot routes
path('farm/<int:farm_id>/chatbot/', views.farm_chatbot, name='farm_chatbot'),
path('farm/<int:farm_id>/chat/', views.send_chat_message, name='send_chat_message'),
```

**No existing routes modified**

---

## Form Integration

### ChatMessageForm

**File**: `farm_app/forms.py`

```python
class ChatMessageForm(forms.Form):
    message = forms.CharField(
        label='Ask me anything about farming or animal feeds',
        widget=forms.Textarea(...)
    )
```

**Used by**:
- `farm_chatbot()` view (displays form)
- `send_chat_message()` view (validates input)

**No changes to existing forms**

---

## Template Integration

### New Template

**File**: `farm_app/templates/farm_app/chatbot.html`

**Features**:
- Standalone template
- Uses Bootstrap styling (matches your app)
- AJAX form submission
- Displays chat history
- Auto-scroll functionality

**Does not modify existing templates**

---

## Admin Integration

### ChatMessageAdmin

**File**: `farm_app/admin.py`

```python
@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'farm', 'created_at', 'message_preview')
    # ... other admin config
```

**Features**:
- View all chat messages
- Filter by user, farm, date
- Search user messages
- Read-only interface
- Message previews

**Added to existing admin registrations**

---

## Settings Integration

### Configuration

**File**: `farm_project/settings.py`

```python
# Added at end of file:
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', None)
```

**Environment variable required**: `OPENAI_API_KEY`

**No changes to existing settings**

---

## Dependencies

### New Requirements

**File**: `requirements.txt`

```
openai==1.3.0
python-dotenv==1.0.0
```

**All existing dependencies unchanged**

---

## Migration

### Database Changes

**File**: `farm_app/migrations/0030_chatmessage.py`

**Creates**:
- `farm_app_chatmessage` table
- Indexes on user_id, farm_id
- Foreign key relationships

**Does not modify existing tables**

---

## Frontend Integration

### HTML Structure

**No existing templates modified**

**New template structure**:
```
chatbot.html
├── Header (Farm Advisor AI)
├── Chat Display Area
│   ├── Welcome message or chat history
│   └── Auto-scroll behavior
├── Input Form (ChatMessageForm)
└── Footer (Navigation)
```

### CSS Classes

**Uses existing Bootstrap classes**:
- `.container`
- `.card`, `.card-header`, `.card-body`
- `.alert` (for messages)
- `.btn` (buttons)
- `.form-group` (form layout)

**No custom CSS required**

### JavaScript

**New script in template**:
- AJAX form submission
- Message display
- Auto-scroll
- Loading states
- Error handling

**No jQuery required** (vanilla JavaScript)

---

## API Layer

### OpenAI Integration

**Services used**:
- `OpenAI` client (from `openai` library)
- `chat.completions.create()` method
- Model: `gpt-3.5-turbo`
- Timeout: 30 seconds (built-in)

**Configuration**:
- API key from environment
- System prompt customizable
- Response length limited to 500 tokens
- Temperature set to 0.7

**No external APIs used except OpenAI**

---

## Authentication Integration

### Login Required

**Decorator**: `@login_required` on all chatbot views

**Behavior**:
- Redirects to `LOGIN_URL` if not authenticated
- Uses Django's built-in auth system
- No custom authentication needed

**No changes to existing auth**

---

## Context Data

### Farm Data Used

When accessing farm-specific chatbot:

```python
# Data automatically included in AI context:
- farm.name
- farm.location
- farm.breed
- farm.total_cattle
- farm.cows_count
- farm.bulls_count
- farm.calf_count
- farm.pregnant_cows
- farm.sick
- farm.Feed
- farm.vaccine1, vaccine2, vaccine3
```

**All existing farm fields accessible**

---

## Database Queries

### Query Patterns

**Get chat history**:
```python
ChatMessage.objects.filter(user=user)
ChatMessage.objects.filter(farm=farm)
```

**Create chat message**:
```python
ChatMessage.objects.create(
    user=user,
    farm=farm,
    user_message=message,
    ai_response=response
)
```

**No modifications to existing models required**

---

## Error Handling

### Exception Handling

**Implemented for**:
- Missing API key
- Network errors
- OpenAI API errors
- Form validation errors
- Database errors

**All errors return user-friendly messages**

---

## Security Implementation

### Access Control

- Login required on all views
- Users can only access their own farms
- Users can only see their own chats
- Admin can see all chats

### Data Protection

- API key in environment (not in code)
- No credentials logged
- CSRF protection on forms
- No sensitive data exposed in responses

---

## Performance Considerations

### Optimization

- AJAX prevents full page reload
- Chat history loaded once per view
- Farm context built only when needed
- Database indexes on frequently queried fields

### Scalability

- One API call per message (not per word)
- Database designed for growth
- Caching could be added if needed

---

## Backward Compatibility

### No Breaking Changes

✅ All existing views work as before
✅ All existing models unchanged (new model added)
✅ All existing URLs work as before
✅ All existing forms work as before
✅ All existing templates work as before
✅ All existing admin interfaces work as before

### Migration Path

1. Install dependencies
2. Run migrations
3. Set API key
4. Start using chatbot

**No changes to existing functionality required**

---

## Extension Points

### How to Customize

**Change AI behavior**:
- Edit system prompt in `send_chat_message()` view
- Change model name in API call
- Adjust temperature parameter

**Add new features**:
- Extend ChatMessageForm for additional inputs
- Add filters to ChatMessageAdmin
- Create new URLs using existing patterns

**Modify UI**:
- Edit `chatbot.html` template
- Override CSS with custom styles
- Add custom JavaScript

---

## Testing Integration

### Test Points

1. Chat creation works
2. OpenAI integration functional
3. Database persistence correct
4. Admin interface displays correctly
5. Authentication enforced
6. Data isolation maintained

### Test Files

```bash
python manage.py test farm_app.tests
```

---

## Deployment Checklist

Before deploying to production:

- [ ] Set `OPENAI_API_KEY` environment variable
- [ ] Run `python manage.py migrate`
- [ ] Set `DEBUG = False` in settings
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set `CSRF_COOKIE_SECURE = True`
- [ ] Set `SESSION_COOKIE_SECURE = True`
- [ ] Enable HTTPS
- [ ] Configure OpenAI spending limits
- [ ] Test with real user accounts
- [ ] Monitor API usage

---

## Integration Summary

| Component | Status | Changes |
|-----------|--------|---------|
| Models | ✅ | Added ChatMessage |
| Views | ✅ | Added 3 functions |
| URLs | ✅ | Added 4 routes |
| Forms | ✅ | Added ChatMessageForm |
| Templates | ✅ | Added chatbot.html |
| Admin | ✅ | Added ChatMessageAdmin |
| Settings | ✅ | Added OPENAI_API_KEY |
| Requirements | ✅ | Added openai, python-dotenv |
| Migrations | ✅ | Added 0030_chatmessage |
| Existing code | ✅ | No modifications |

---

## Reference Links

Within Project:
- [QUICK_START.md](QUICK_START.md) - Quick setup guide
- [CHATBOT_SETUP.md](CHATBOT_SETUP.md) - Detailed setup
- [TESTING_GUIDE.md](TESTING_GUIDE.md) - Testing procedures
- [MIGRATION_INFO.md](MIGRATION_INFO.md) - Database migration details

External:
- [OpenAI API Docs](https://platform.openai.com/docs)
- [Django Documentation](https://docs.djangoproject.com/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/)

---

**Integration complete and production-ready!** 🚀
