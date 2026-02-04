# Database Migration Information

## ChatMessage Model Migration

**File**: `farm_app/migrations/0030_chatmessage.py`

This migration creates the `ChatMessage` table with the following structure:

### Table Schema

| Column | Type | Constraints |
|--------|------|-----------|
| id | BigAutoField | PRIMARY KEY |
| user_message | TextField | NOT NULL |
| ai_response | TextField | NOT NULL |
| created_at | DateTimeField | NOT NULL, auto-set on creation |
| farm_id | ForeignKey | Nullable, references Farm |
| user_id | ForeignKey | NOT NULL, references User |

### Relationships

- **User** (Foreign Key)
  - One user can have many chat messages
  - Deleting a user deletes their chat history

- **Farm** (Foreign Key, Optional)
  - One farm can have many chat messages
  - Deleting a farm deletes associated chats
  - Null when chatting with global chatbot

### Indexes & Ordering

- Default ordering: By `created_at` descending (newest first)
- Useful indexes: user_id, farm_id, created_at

## How to Apply the Migration

### Before First Use

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Apply all migrations**:
   ```bash
   python manage.py migrate
   ```

3. **Verify success**:
   ```bash
   python manage.py showmigrations farm_app
   ```

You should see:
```
[ X] 0030_chatmessage
```

### If You Have Existing Database

The migration will:
- Create the new `ChatMessage` table
- Add foreign key constraints
- Set up proper indexing

No existing data will be affected.

### Reverting the Migration

If needed, you can undo this migration:

```bash
python manage.py migrate farm_app 0029_abattoir
```

This will:
- Drop the ChatMessage table
- Lose all stored conversations
- Revert to previous state

## Checking Migration Status

```bash
# Show all migrations
python manage.py showmigrations farm_app

# Show detailed migration info
python manage.py sqlmigrate farm_app 0030

# Verify database state
python manage.py dbshell
sqlite> SELECT COUNT(*) FROM farm_app_chatmessage;
```

## Backup Recommendations

Before running migrations in production:

1. **Backup database**:
   ```bash
   # SQLite
   cp db.sqlite3 db.sqlite3.backup
   ```

2. **Test migrations locally first**
3. **Keep backup for rollback ability**

## Database Schema View

```sql
CREATE TABLE farm_app_chatmessage (
    id BIGINT PRIMARY KEY,
    user_message TEXT NOT NULL,
    ai_response TEXT NOT NULL,
    created_at DATETIME NOT NULL,
    farm_id INT,
    user_id INT NOT NULL,
    FOREIGN KEY (farm_id) REFERENCES farm_app_farm(id),
    FOREIGN KEY (user_id) REFERENCES auth_user(id)
);

CREATE INDEX farm_app_chatmessage_user_id ON farm_app_chatmessage(user_id);
CREATE INDEX farm_app_chatmessage_farm_id ON farm_app_chatmessage(farm_id);
```

## Troubleshooting Migrations

### Issue: "No changes detected"
```
Solution: Ensure models.py has ChatMessage class
```

### Issue: "Migration conflicts"
```
Solution: Resolve migration order:
python manage.py showmigrations farm_app
```

### Issue: "Database is locked"
```
Solution: Close other connections to db.sqlite3
Close any other Django instances
```

### Issue: "Duplicate migration name"
```
Solution: Rename migration if it exists:
mv 0030_chatmessage.py 0031_chatmessage.py
Update the class name inside
```

## Post-Migration Steps

After successful migration:

1. **Create a superuser** (if needed):
   ```bash
   python manage.py createsuperuser
   ```

2. **Access admin panel**:
   ```
   http://localhost:8000/admin/
   farm_app → Chat Messages
   ```

3. **Test chatbot functionality**:
   ```
   Visit http://localhost:8000/chatbot/
   Send a test message
   Verify it appears in admin
   ```

## Migration File Contents

The migration creates:

```python
class Migration(migrations.Migration):
    dependencies = [
        ('farm_app', '0029_abattoir'),
    ]
    
    operations = [
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                # ID, user_message, ai_response fields
                # created_at, farm, user foreign keys
            ],
        ),
    ]
```

## Related Models

The ChatMessage model relates to:

**User** (Django Auth)
- One user can create multiple chat messages
- User deletion cascades to chat deletion

**Farm** (farm_app.models)
- One farm can have multiple chat messages  
- Farm deletion cascades to chat deletion
- Optional relationship (global chats have null farm)

## Query Examples

```python
# Get all chats for a user
ChatMessage.objects.filter(user=request.user)

# Get chats for specific farm
ChatMessage.objects.filter(farm=farm)

# Get recent chats (last 10)
ChatMessage.objects.order_by('-created_at')[:10]

# Get chats from today
from django.utils import timezone
today = timezone.now().date()
ChatMessage.objects.filter(created_at__date=today)

# Search user messages
ChatMessage.objects.filter(user_message__icontains='feed')

# Delete old chats (older than 30 days)
from datetime import timedelta
cutoff = timezone.now() - timedelta(days=30)
ChatMessage.objects.filter(created_at__lt=cutoff).delete()
```

## Performance Considerations

- Table will grow with usage
- Consider archiving old chats periodically
- Add database indexes if >10,000 chats
- Monitor query performance

## Next Steps

1. ✅ Review this migration info
2. ✅ Run `python manage.py migrate`
3. ✅ Start using the chatbot
4. ✅ Monitor database size
5. ✅ Archive old chats as needed (optional)
