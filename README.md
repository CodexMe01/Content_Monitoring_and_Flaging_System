# Content Monitoring and Flagging System

## Setup

1. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # Windows
   ```

2. Install dependencies:
   ```bash
   pip install django djangorestframework
   ```

3. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. Start the server:
   ```bash
   python manage.py runserver
   ```

## Keyword Scoring

When content is scanned, it is evaluated against all active keywords to generate a score:
- **Exact Match in Title**: Score of 100
- **Partial Match in Title**: Score of max 70
- **Partial Match in Body**: Score of max 40

A flag is generated for any content that scores above 0.

## Review Workflow & Suppression Rules

The system includes a suppression mechanism to prevent repeated flagging of unchanged irrelevant content:
- If a flag is marked as `irrelevant`, it will be suppressed.
- If the associated content is later updated (either its body text changes or the `last_updated` timestamp is newer), the flag will be re-evaluated. If it still matches a keyword, its status will be reset to `pending` and it will resurface for review.

## API Documentation

### 1. List Keywords
```bash
curl -X GET http://127.0.0.1:8000/api/keywords/
```

### 2. Create a Keyword
```bash
curl -X POST http://127.0.0.1:8000/api/keywords/ \
-H "Content-Type: application/json" \
-d '{"name": "badword"}'
```

### 3. Scan Content
```bash
curl -X POST http://127.0.0.1:8000/api/scan/ \
-H "Content-Type: application/json" \
-d '[
  {
    "title": "A new badword appears",
    "source": "NewsSource",
    "body": "Nothing much here.",
    "last_updated": "2023-10-01T12:00:00Z"
  }
]'
```

### 4. List Flags
```bash
curl -X GET http://127.0.0.1:8000/api/flags/
```

### 5. Update Flag Status
```bash
curl -X PATCH http://127.0.0.1:8000/api/flags/1/ \
-H "Content-Type: application/json" \
-d '{"status": "irrelevant"}'
```

## Running Tests
Run the test suite to verify the scanning logic:
```bash
python manage.py test content_api
```
