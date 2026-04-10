Let's do it! Go to your GitHub repo → click on README.md → click the pencil icon (Edit) → delete everything and paste this:
markdown<div align="center">

# 🎬 IMDb Clone — REST API Backend

*A production-ready movie database API inspired by IMDb*

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-4.2-092E20?style=for-the-badge&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/REST_Framework-3.14-ff1709?style=for-the-badge)
![JWT](https://img.shields.io/badge/Auth-JWT-black?style=for-the-badge&logo=jsonwebtokens)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?style=for-the-badge&logo=sqlite)

[Features](#-features) • [Quick Start](#-quick-start) • [API Endpoints](#-api-endpoints) • [Tech Stack](#-tech-stack)

</div>

---

## 📌 About

A fully featured **Movie Database REST API** built with Django REST Framework. It lets you browse movies, rate them, write reviews, manage a watchlist — all secured with JWT authentication. Think IMDb, but as a backend service any frontend can plug into.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
|  **JWT Auth** | Register, login, logout with token blacklisting |
|  **Movie Database** | Full CRUD — genres, cast, directors, writers |
|  **Ratings** | 1–10 scoring, averages auto-calculated via Django Signals |
|  **Reviews** | Write reviews, upvote helpful ones |
|  **Watchlist** | Personal per-user movie lists |
|  **Search & Filter** | Filter by year, genre, rating, language |
|  **API Docs** | Auto-generated Swagger UI + ReDoc |
|  **Admin Panel** | Full Django admin with inline cast management |

---

## 🚀 Quick Start

```bash
git clone https://github.com/CoderParva/Imbd-api-backend.git
cd Imbd-api-backend

python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate
python manage.py seed_db      # loads 8 movies, 16 genres, 10 people
python manage.py createsuperuser
python manage.py runserver
```

> Server runs at `http://127.0.0.1:8000`

---

##  API Documentation

| URL | Description |
|-----|-------------|
| [`/api/docs/`](http://127.0.0.1:8000/api/docs/) | ✅ Swagger UI — interactive explorer |
| [`/api/redoc/`](http://127.0.0.1:8000/api/redoc/) | 📄 ReDoc — clean reference |
| [`/admin/`](http://127.0.0.1:8000/admin/) | 🔧 Django Admin panel |

---

##  API Endpoints

###  Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/auth/register/` | Create new account |
| `POST` | `/api/v1/auth/login/` | Login → returns JWT tokens |
| `POST` | `/api/v1/auth/logout/` | Blacklist refresh token |
| `POST` | `/api/v1/auth/token/refresh/` | Get new access token |
| `GET/PUT` | `/api/v1/auth/profile/` | View / update profile |
| `PUT` | `/api/v1/auth/change-password/` | Change password |

###  Movies
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/movies/` | List all movies (paginated) |
| `GET` | `/api/v1/movies/<slug>/` | Movie detail |
| `GET` | `/api/v1/movies/top-rated/` | Top rated movies |
| `GET` | `/api/v1/movies/featured/` | Featured movies |
| `POST` | `/api/v1/movies/` | Create movie *(admin only)* |
| `PUT/PATCH` | `/api/v1/movies/<slug>/` | Update movie *(admin only)* |
| `DELETE` | `/api/v1/movies/<slug>/` | Delete movie *(admin only)* |

###  Ratings & Reviews
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/movies/<slug>/rate/` | Rate a movie (1–10) |
| `DELETE` | `/api/v1/movies/<slug>/rate/` | Remove your rating |
| `GET/POST` | `/api/v1/reviews/` | List / write reviews |
| `PUT/DELETE` | `/api/v1/reviews/<id>/` | Edit / delete your review |
| `POST` | `/api/v1/reviews/<id>/helpful/` | Upvote a review |

###  Watchlist & More
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET/POST` | `/api/v1/watchlist/` | View / add to watchlist |
| `DELETE` | `/api/v1/watchlist/<id>/` | Remove from watchlist |
| `GET` | `/api/v1/genres/` | List all genres |
| `GET` | `/api/v1/people/` | List all people |

---

##  Filtering & Search

```bash
# Filter by genre
GET /api/v1/movies/?genre=action

# Filter by year range
GET /api/v1/movies/?release_year_min=2000&release_year_max=2020

# Filter by minimum rating
GET /api/v1/movies/?rating_min=8.0

# Full-text search
GET /api/v1/movies/?search=nolan

# Sort by rating
GET /api/v1/movies/?ordering=-avg_rating

# Combine filters
GET /api/v1/movies/?genre=sci-fi&release_year_min=2010&ordering=-avg_rating
```

---

##  Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.12 |
| Framework | Django 4.2 |
| API Layer | Django REST Framework 3.14 |
| Authentication | SimpleJWT + Token Blacklist |
| Filtering | django-filter |
| API Docs | drf-spectacular (Swagger / ReDoc) |
| Database | SQLite (dev) → PostgreSQL (prod) |
| Image Handling | Pillow |

---

##  Database Models

```
CustomUser    →  Email-based auth, bio, avatar
Movie         →  Title, synopsis, poster, trailer, budget, revenue
Genre         →  Slug-based categorization
Person        →  Actors, directors, writers
CastMember    →  Through model with character names + order
Rating        →  1–10 score per user per movie
Review        →  Full text + helpful votes
Watchlist     →  Per-user movie lists
```

---

##  Authentication Flow

```
POST /auth/register/  →  Create account
POST /auth/login/     →  Get access token (60 min) + refresh token (7 days)
                         Add to requests: Authorization: Bearer <access_token>
POST /auth/logout/    →  Refresh token blacklisted, can never be reused
POST /token/refresh/  →  Get new access token using refresh token
```

---

<div align="center">

Made with ❤️ by [CoderParva](https://github.com/CoderParva)

 Star this repo if you found it useful!

</div>
