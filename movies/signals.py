from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg
from .models import Rating


def update_movie_rating(movie):
    """Recalculate and persist avg_rating + total_ratings on the movie."""
    result = movie.ratings.aggregate(avg=Avg('score'))
    movie.avg_rating = round(result['avg'] or 0, 2)
    movie.total_ratings = movie.ratings.count()
    movie.save(update_fields=['avg_rating', 'total_ratings'])


@receiver(post_save, sender=Rating)
def on_rating_save(sender, instance, **kwargs):
    update_movie_rating(instance.movie)


@receiver(post_delete, sender=Rating)
def on_rating_delete(sender, instance, **kwargs):
    update_movie_rating(instance.movie)
