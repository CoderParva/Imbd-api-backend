from django.shortcuts import get_object_or_404
from rest_framework import generics, status, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Genre, Person, Movie, Rating, Review, Watchlist
from .serializers import (
    GenreSerializer,
    PersonSerializer,
    MovieListSerializer,
    MovieDetailSerializer,
    RatingSerializer,
    ReviewSerializer,
    WatchlistSerializer,
)
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from .filters import MovieFilter


# ── Genre ──────────────────────────────────────────────────────────────────────

class GenreListCreateView(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['name']


class GenreDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'slug'


# ── Person ─────────────────────────────────────────────────────────────────────

class PersonListCreateView(generics.ListCreateAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['name']
    ordering_fields = ['name']


class PersonDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = [IsAdminOrReadOnly]


# ── Movie ──────────────────────────────────────────────────────────────────────

class MovieViewSet(viewsets.ModelViewSet):
    """
    Full CRUD for movies.
    List / Retrieve — public
    Create / Update / Destroy — admin only
    """
    queryset = Movie.objects.prefetch_related('genres', 'directors', 'writers', 'cast_members__person')
    permission_classes = [IsAdminOrReadOnly]
    filterset_class = MovieFilter
    search_fields = ['title', 'original_title', 'synopsis', 'directors__name', 'cast__name']
    ordering_fields = ['release_year', 'avg_rating', 'total_ratings', 'title', 'created_at']
    ordering = ['-release_year']
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'list':
            return MovieListSerializer
        return MovieDetailSerializer

    @action(detail=True, methods=['get'], url_path='reviews')
    def movie_reviews(self, request, slug=None):
        """All reviews for a specific movie."""
        movie = self.get_object()
        reviews = movie.reviews.select_related('user')
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='ratings')
    def movie_ratings(self, request, slug=None):
        """Aggregate ratings info for a movie."""
        movie = self.get_object()
        return Response({
            'avg_rating': movie.avg_rating,
            'total_ratings': movie.total_ratings,
        })

    @action(detail=False, methods=['get'], url_path='featured')
    def featured(self, request):
        qs = self.get_queryset().filter(is_featured=True)
        serializer = MovieListSerializer(qs, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='top-rated')
    def top_rated(self, request):
        qs = self.get_queryset().filter(total_ratings__gte=5).order_by('-avg_rating')[:50]
        serializer = MovieListSerializer(qs, many=True, context={'request': request})
        return Response(serializer.data)


# ── Rating ─────────────────────────────────────────────────────────────────────

class RateMovieView(APIView):
    """POST to rate, DELETE to remove your rating."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, slug):
        movie = get_object_or_404(Movie, slug=slug)
        serializer = RatingSerializer(data={**request.data, 'movie': movie.id})
        if serializer.is_valid():
            Rating.objects.update_or_create(
                user=request.user,
                movie=movie,
                defaults={'score': serializer.validated_data['score']},
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):
        movie = get_object_or_404(Movie, slug=slug)
        deleted, _ = Rating.objects.filter(user=request.user, movie=movie).delete()
        if deleted:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': 'Rating not found.'}, status=status.HTTP_404_NOT_FOUND)


# ── Review ─────────────────────────────────────────────────────────────────────

class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    search_fields = ['title', 'body']
    ordering_fields = ['helpful_votes', 'created_at']

    def get_queryset(self):
        return Review.objects.select_related('user', 'movie').all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.select_related('user', 'movie')
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class MarkReviewHelpfulView(APIView):
    """Upvote a review as helpful."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        review = get_object_or_404(Review, pk=pk)
        review.helpful_votes += 1
        review.save(update_fields=['helpful_votes'])
        return Response({'helpful_votes': review.helpful_votes})


# ── Watchlist ──────────────────────────────────────────────────────────────────

class WatchlistView(generics.ListCreateAPIView):
    serializer_class = WatchlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Watchlist.objects.filter(user=self.request.user).select_related('movie')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WatchlistItemView(generics.DestroyAPIView):
    serializer_class = WatchlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Watchlist.objects.filter(user=self.request.user)
