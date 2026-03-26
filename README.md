# Social Media API

---

## Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Project Structure](#project-structure)
4. [API Endpoints](#api-endpoints)
5. [Run Locally](#run-locally)
6. [Run Redis for Celery](#run-redis-for-celery)
7. [Run Celery Worker](#run-celery-worker)
8. [Testing](#testing)
9. [Technologies](#technologies)

---

## Project Overview

Social Media API is a Django REST Framework backend for a small social platform. It includes a custom user model, auto-created profiles, posts with hashtags, follow relationships, likes, comments, JWT authentication, and Celery integration backed by Redis.

The project exposes REST endpoints for the main social features and includes Swagger/OpenAPI documentation plus automated tests for each app package.

---

## Features

- Custom user model with email-based authentication
- JWT access and refresh tokens
- Auto-created profile for each new user
- Post creation with hashtag normalization and filtering
- Follow system with self-follow prevention
- Like and comment interactions
- Django admin registration for all models
- OpenAPI schema and Swagger UI via drf-spectacular
- Celery task support with Redis broker/result backend
- App-level automated tests for users, profiles, posts, follows, and interactions

---

## Project Structure

```text
social-media-api/
|-- config/                         # Django project settings, routing, Celery bootstrap, shared permissions
|   |-- settings.py
|   |-- urls.py
|   |-- celery.py
|   |-- permissions.py
|   |-- asgi.py
|   |-- wsgi.py
|   `-- __init__.py
|-- users/                          # Custom user model, serializer, viewset, admin, tests
|-- profiles/                       # Profile model, signals, serializer, viewset, admin, tests
|-- posts/                          # Posts and hashtags
|-- follows/                        # Follow relations between users
|-- interactions/                   # Likes, comments, and Celery tasks
|   `-- tasks.py                    # Example async task: post engagement summary
|-- manage.py
|-- requirements.txt
|-- README.md
|-- README_example.md
`-- db.sqlite3
```

App responsibilities:

- `users`: custom `User` model and JWT-authenticated user endpoints
- `profiles`: one-to-one user profiles created via signals
- `posts`: `Post` and `Hashtag` models with filtering by author/hashtag
- `follows`: follow/unfollow relationships
- `interactions`: likes, comments, and async task definitions

---

## API Endpoints

Base URL: `http://127.0.0.1:8000/`

Main routes:

- `/api/users/`
- `/api/users/me/`
- `/api/profiles/`
- `/api/profiles/me/`
- `/api/hashtags/`
- `/api/posts/`
- `/api/follows/`
- `/api/likes/`
- `/api/comments/`

Authentication and docs:

- `/api/token/`
- `/api/token/refresh/`
- `/api/token/verify/`
- `/api/schema/`
- `/api/docs/`
- `/admin/`

Example JWT request:

```http
POST /api/token/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "your_password"
}
```

Use the access token in authenticated requests:

```text
Authorization: Bearer <access_token>
```

---

## Run Locally

### Prerequisites

- Python 3.12+
- `venv`
- Redis server on `127.0.0.1:6379`

### Setup

1. Clone the repository and move into the project directory:

```bash
git clone https://github.com/mishagitcode/social-media-api
cd social-media-api
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create an environment file:

```bash
cp .env.example .env
```

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

5. Apply migrations:

```bash
python manage.py migrate
```

6. Optionally create a superuser:

```bash
python manage.py createsuperuser
```

7. Start the Django development server:

```bash
python manage.py runserver
```

---

## Run Redis for Celery

If Redis is not installed directly on your machine, you can run it with Docker:

```powershell
docker run -d --name social-media-api-redis -p 6379:6379 redis:7-alpine
```

If the container already exists:

```powershell
docker start social-media-api-redis
```

Default Celery Redis settings from `.env.example`:

```text
CELERY_BROKER_URL=redis://127.0.0.1:6379/0
CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/0
```

---

## Run Celery Worker

Start a Celery worker in a separate terminal:

```powershell
celery -A config worker --pool=solo -l info
```

The project currently includes an example async task in `interactions/tasks.py` that calculates a post engagement summary.

---

## Testing

Run the full test suite:

```bash
python manage.py test
```

Run the app package tests explicitly:

```bash
python manage.py test users profiles posts follows interactions
```

---

## Technologies

- Python 3.12
- Django 6
- Django REST Framework
- Simple JWT
- Celery
- Redis
- drf-spectacular
- SQLite
- Docker (optional, for Redis)

---

Implemented by [mishagitcode](https://github.com/mishagitcode)