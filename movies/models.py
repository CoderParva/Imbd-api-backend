from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Person(models.Model):
    ROLE_CHOICES = [
        ('actor', 'Actor'),
        ('director', 'Director'),
        ('writer', 'Writer'),
        ('producer', 'Producer'),
    ]
    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    birth_place = models.CharField(max_length=200, blank=True)
    photo = models.ImageField(upload_to='persons/', null=True, blank=True)
    roles = models.JSONField(default=list)  # ['actor', 'director']

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'People'


class Movie(models.Model):
    CONTENT_RATING_CHOICES = [
        ('G', 'G'), ('PG', 'PG'), ('PG-13', 'PG-13'),
        ('R', 'R'), ('NC-17', 'NC-17'), ('NR', 'Not Rated'),
    ]

    title = models.CharField(max_length=300)
    original_title = models.CharField(max_length=300, blank=True)
    slug = models.SlugField(unique=True, max_length=350)
    tagline = models.CharField(max_length=500, blank=True)
    synopsis = models.TextField()
    release_year = models.PositiveIntegerField()
    runtime_minutes = models.PositiveIntegerField(null=True, blank=True)
    content_rating = models.CharField(max_length=10, choices=CONTENT_RATING_CHOICES, default='NR')
    poster = models.ImageField(upload_to='posters/', null=True, blank=True)
    backdrop = models.ImageField(upload_to='backdrops/', null=True, blank=True)
    trailer_url = models.URLField(blank=True)
    budget = models.BigIntegerField(null=True, blank=True, help_text='USD')
    revenue = models.BigIntegerField(null=True, blank=True, help_text='USD')
    language = models.CharField(max_length=10, default='en')
    country = models.CharField(max_length=100, blank=True)
    genres = models.ManyToManyField(Genre, related_name='movies', blank=True)
    directors = models.ManyToManyField(Person, related_name='directed', blank=True)
    writers = models.ManyToManyField(Person, related_name='written', blank=True)
    cast = models.ManyToManyField(Person, through='CastMember', related_name='appeared_in', blank=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Cached aggregates (updated via signals)
    avg_rating = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    total_ratings = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.title} ({self.release_year})"

    class Meta:
        ordering = ['-release_year', 'title']


class CastMember(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='cast_members')
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    character_name = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        unique_together = ('movie', 'person')

    def __str__(self):
        return f"{self.person.name} as {self.character_name} in {self.movie.title}"


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='ratings')
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'movie')

    def __str__(self):
        return f"{self.user.email} → {self.movie.title}: {self.score}/10"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    title = models.CharField(max_length=200)
    body = models.TextField()
    contains_spoilers = models.BooleanField(default=False)
    helpful_votes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'movie')
        ordering = ['-helpful_votes', '-created_at']

    def __str__(self):
        return f"Review by {self.user.email} for {self.movie.title}"


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlist')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='watchlisted_by')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie')
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.user.email}'s watchlist: {self.movie.title}"
