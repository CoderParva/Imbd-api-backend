# 🎬 IMDb Clone — Django REST API

A production-ready movie database REST API built with Django REST Framework, featuring JWT authentication, full CRUD for movies, ratings, reviews, and watchlists.

## ✨ Features

- **JWT Authentication** — Register, login, logout (token blacklisting), refresh tokens
- **Movie Database** — Full CRUD with genres, cast, directors, writers
- **Smart Filtering** — Filter by year range, rating, genre, language, content rating
- **Search** — Full-text search across titles, synopsis, cast, and directors
- **Ratings System** — 1–10 scoring with auto-calculated averages via Django signals
- **Reviews** — Create reviews, upvote helpful ones
- **Watchlist** — Personal per-user watchlists
- **API Docs** — Auto-generated Swagger UI & ReDoc via drf-spectacular
- **Admin Panel** — Full Django admin with inline cast management

## 🚀 Quick Start

```bash
# 1. Clone and enter directory
cd IMDB_api_backend_project

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations
python manage.py migrate

# 5. Seed with sample data
python manage.py seed_db

# 6. Create superuser (for admin)
python manage.py createsuperuser

# 7. Start server
python manage.py runserver
```

## 📖 API Documentation

| URL | Description |
|-----|-------------|
| `http://127.0.0.1:8000/api/docs/` | Swagger UI |
| `http://127.0.0.1:8000/api/redoc/` | ReDoc |
| `http://127.0.0.1:8000/admin/` | Django Admin |

## 🔗 API Endpoints

### Authentication
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/v1/auth/register/` | ❌ | Create account |
| POST | `/api/v1/auth/login/` | ❌ | Login → get tokens |
| POST | `/api/v1/auth/logout/` | ✅ | Blacklist refresh token |
| POST | `/api/v1/auth/token/refresh/` | ❌ | Refresh access token |
| GET/PUT | `/api/v1/auth/profile/` | ✅ | View / update profile |
| PUT | `/api/v1/auth/change-password/` | ✅ | Change password |

### Movies
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/v1/movies/` | ❌ | List movies (paginated) |
| POST | `/api/v1/movies/` | 🔑 Admin | Create movie |
| GET | `/api/v1/movies/<slug>/` | ❌ | Movie detail |
| PUT/PATCH | `/api/v1/movies/<slug>/` | 🔑 Admin | Update movie |
| DELETE | `/api/v1/movies/<slug>/` | 🔑 Admin | Delete movie |
| GET | `/api/v1/movies/top-rated/` | ❌ | Top rated movies |
| GET | `/api/v1/movies/featured/` | ❌ | Featured movies |
| GET | `/api/v1/movies/<slug>/reviews/` | ❌ | Movie's reviews |
| GET | `/api/v1/movies/<slug>/ratings/` | ❌ | Movie's rating stats |

### Ratings & Reviews
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/v1/movies/<slug>/rate/` | ✅ | Rate a movie (1–10) |
| DELETE | `/api/v1/movies/<slug>/rate/` | ✅ | Remove your rating |
| GET | `/api/v1/reviews/` | ❌ | All reviews |
| POST | `/api/v1/reviews/` | ✅ | Write a review |
| GET/PUT/DELETE | `/api/v1/reviews/<id>/` | ✅ Owner | Review detail |
| POST | `/api/v1/reviews/<id>/helpful/` | ✅ | Mark review helpful |

### Genres & People
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/v1/genres/` | ❌ | List genres |
| POST | `/api/v1/genres/` | 🔑 Admin | Create genre |
| GET | `/api/v1/genres/<slug>/` | ❌ | Genre detail |
| GET | `/api/v1/people/` | ❌ | List people |
| POST | `/api/v1/people/` | 🔑 Admin | Create person |
| GET | `/api/v1/people/<id>/` | ❌ | Person detail |

### Watchlist
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/v1/watchlist/` | ✅ | Your watchlist |
| POST | `/api/v1/watchlist/` | ✅ | Add to watchlist |
| DELETE | `/api/v1/watchlist/<id>/` | ✅ | Remove from watchlist |

## 🔍 Filtering & Search

```
# Filter by genre slug
GET /api/v1/movies/?genre=action

# Filter by year range
GET /api/v1/movies/?release_year_min=2000&release_year_max=2020

# Filter by minimum rating
GET /api/v1/movies/?rating_min=8.0

# Filter featured movies
GET /api/v1/movies/?is_featured=true

# Full-text search
GET /api/v1/movies/?search=nolan

# Sort results
GET /api/v1/movies/?ordering=-avg_rating

# Combine filters
GET /api/v1/movies/?genre=sci-fi&release_year_min=2010&ordering=-avg_rating
```

## 🔐 Authentication Usage

```bash
# 1. Register
curl -X POST http://localhost:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"john","email":"john@example.com","password":"pass123!","password2":"pass123!"}'

# 2. Login
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"john@example.com","password":"pass123!"}'

# 3. Use token
curl http://localhost:8000/api/v1/watchlist/ \
  -H "Authorization: Bearer <access_token>"
```

## 🏗️ Project Structure

```
IMDB_api_backend_project/
├── config/
│   ├── settings.py          # Django settings
│   ├── urls.py              # Root URL config
│   └── wsgi.py
├── accounts/                # Auth app
│   ├── models.py            # CustomUser model
│   ├── serializers.py       # Auth serializers
│   ├── views.py             # Auth views
│   └── urls.py
├── movies/                  # Core app
│   ├── models.py            # Movie, Genre, Person, Rating, Review, Watchlist
│   ├── serializers.py       # All serializers
│   ├── views.py             # All views + ViewSets
│   ├── filters.py           # MovieFilter
│   ├── permissions.py       # Custom permissions
│   ├── signals.py           # Auto-update avg_rating
│   ├── admin.py             # Admin configuration
│   └── management/
│       └── commands/
│           └── seed_db.py   # Sample data seeder
├── requirements.txt
├── .env.example
└── README.md
```
