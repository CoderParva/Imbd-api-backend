from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    GenreListCreateView, GenreDetailView,
    PersonListCreateView, PersonDetailView,
    MovieViewSet,
    RateMovieView,
    ReviewListCreateView, ReviewDetailView, MarkReviewHelpfulView,
    WatchlistView, WatchlistItemView,
)

router = DefaultRouter()
router.register(r'movies', MovieViewSet, basename='movie')

urlpatterns = [
    # Movies (via router)
    path('', include(router.urls)),

    # Genres
    path('genres/', GenreListCreateView.as_view(), name='genre-list'),
    path('genres/<slug:slug>/', GenreDetailView.as_view(), name='genre-detail'),

    # People
    path('people/', PersonListCreateView.as_view(), name='person-list'),
    path('people/<int:pk>/', PersonDetailView.as_view(), name='person-detail'),

    # Ratings (nested under movie)
    path('movies/<slug:slug>/rate/', RateMovieView.as_view(), name='movie-rate'),

    # Reviews
    path('reviews/', ReviewListCreateView.as_view(), name='review-list'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
    path('reviews/<int:pk>/helpful/', MarkReviewHelpfulView.as_view(), name='review-helpful'),

    # Watchlist
    path('watchlist/', WatchlistView.as_view(), name='watchlist'),
    path('watchlist/<int:pk>/', WatchlistItemView.as_view(), name='watchlist-item'),
]
