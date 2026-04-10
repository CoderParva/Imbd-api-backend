from rest_framework import serializers
from .models import Genre, Person, Movie, CastMember, Rating, Review, Watchlist
from django.contrib.auth import get_user_model

User = get_user_model()


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name', 'slug')


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('id', 'name', 'bio', 'birth_date', 'birth_place', 'photo', 'roles')


class CastMemberSerializer(serializers.ModelSerializer):
    person = PersonSerializer(read_only=True)
    person_id = serializers.PrimaryKeyRelatedField(
        queryset=Person.objects.all(), source='person', write_only=True
    )

    class Meta:
        model = CastMember
        fields = ('id', 'person', 'person_id', 'character_name', 'order')


# ── Movie Serializers ──────────────────────────────────────────────────────────

class MovieListSerializer(serializers.ModelSerializer):
    """Compact serializer for list views."""
    genres = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = (
            'id', 'title', 'slug', 'release_year', 'runtime_minutes',
            'content_rating', 'poster', 'genres', 'avg_rating', 'total_ratings',
            'language', 'is_featured',
        )


class MovieDetailSerializer(serializers.ModelSerializer):
    """Full serializer for detail views."""
    genres = GenreSerializer(many=True, read_only=True)
    directors = PersonSerializer(many=True, read_only=True)
    writers = PersonSerializer(many=True, read_only=True)
    cast_members = CastMemberSerializer(many=True, read_only=True)

    genre_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Genre.objects.all(), source='genres', write_only=True, required=False
    )
    director_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Person.objects.all(), source='directors', write_only=True, required=False
    )
    writer_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Person.objects.all(), source='writers', write_only=True, required=False
    )

    class Meta:
        model = Movie
        fields = (
            'id', 'title', 'original_title', 'slug', 'tagline', 'synopsis',
            'release_year', 'runtime_minutes', 'content_rating', 'poster',
            'backdrop', 'trailer_url', 'budget', 'revenue', 'language',
            'country', 'genres', 'genre_ids', 'directors', 'director_ids',
            'writers', 'writer_ids', 'cast_members', 'avg_rating', 'total_ratings',
            'is_featured', 'created_at', 'updated_at',
        )
        read_only_fields = ('avg_rating', 'total_ratings', 'created_at', 'updated_at')


# ── Rating ─────────────────────────────────────────────────────────────────────

class RatingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Rating
        fields = ('id', 'user', 'movie', 'score', 'created_at', 'updated_at')
        read_only_fields = ('user', 'created_at', 'updated_at')


# ── Review ─────────────────────────────────────────────────────────────────────

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    movie_title = serializers.CharField(source='movie.title', read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'user', 'movie', 'movie_title', 'title', 'body',
                  'contains_spoilers', 'helpful_votes', 'created_at', 'updated_at')
        read_only_fields = ('user', 'helpful_votes', 'created_at', 'updated_at')


# ── Watchlist ──────────────────────────────────────────────────────────────────

class WatchlistSerializer(serializers.ModelSerializer):
    movie = MovieListSerializer(read_only=True)
    movie_id = serializers.PrimaryKeyRelatedField(
        queryset=Movie.objects.all(), source='movie', write_only=True
    )

    class Meta:
        model = Watchlist
        fields = ('id', 'movie', 'movie_id', 'added_at')
        read_only_fields = ('added_at',)
