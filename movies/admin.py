from django.contrib import admin
from .models import Genre, Person, Movie, CastMember, Rating, Review, Watchlist


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'birth_date', 'birth_place')
    search_fields = ('name',)


class CastMemberInline(admin.TabularInline):
    model = CastMember
    extra = 1


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_year', 'content_rating', 'avg_rating', 'total_ratings', 'is_featured')
    list_filter = ('release_year', 'content_rating', 'is_featured', 'genres')
    search_fields = ('title', 'synopsis')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('genres', 'directors', 'writers')
    inlines = [CastMemberInline]
    readonly_fields = ('avg_rating', 'total_ratings', 'created_at', 'updated_at')


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'score', 'created_at')
    list_filter = ('score',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'title', 'helpful_votes', 'created_at')
    search_fields = ('title', 'body')


@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'added_at')
