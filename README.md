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

## API Documentation

### 1. Create a Keyword
```bash
curl -X POST http://127.0.0.1:8000/api/keywords/ \
-H "Content-Type: application/json" \
-d '{"name": "badword"}'
```

### 2. Scan Content
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

### 3. List Flags
```bash
curl -X GET http://127.0.0.1:8000/api/flags/
```

### 4. Update Flag Status
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
