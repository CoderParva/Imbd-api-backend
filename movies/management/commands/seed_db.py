"""
Management command to seed the database with sample IMDb-style data.
Usage: python manage.py seed_db
"""
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from movies.models import Genre, Person, Movie

GENRES = [
    'Action', 'Adventure', 'Animation', 'Biography', 'Comedy',
    'Crime', 'Documentary', 'Drama', 'Fantasy', 'Horror',
    'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'Western',
]

PEOPLE = [
    {'name': 'Christopher Nolan', 'roles': ['director', 'writer']},
    {'name': 'Steven Spielberg', 'roles': ['director', 'producer']},
    {'name': 'Quentin Tarantino', 'roles': ['director', 'writer']},
    {'name': 'Leonardo DiCaprio', 'roles': ['actor']},
    {'name': 'Meryl Streep', 'roles': ['actor']},
    {'name': 'Tom Hanks', 'roles': ['actor', 'producer']},
    {'name': 'Cate Blanchett', 'roles': ['actor']},
    {'name': 'Denzel Washington', 'roles': ['actor', 'director']},
    {'name': 'Martin Scorsese', 'roles': ['director', 'producer']},
    {'name': 'Francis Ford Coppola', 'roles': ['director', 'writer', 'producer']},
]

MOVIES = [
    {
        'title': 'Inception',
        'release_year': 2010,
        'runtime_minutes': 148,
        'content_rating': 'PG-13',
        'synopsis': 'A thief who steals corporate secrets through dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.',
        'genres': ['Action', 'Sci-Fi', 'Thriller'],
        'directors': ['Christopher Nolan'],
        'language': 'en',
        'budget': 160000000,
        'revenue': 836836967,
        'is_featured': True,
    },
    {
        'title': 'The Dark Knight',
        'release_year': 2008,
        'runtime_minutes': 152,
        'content_rating': 'PG-13',
        'synopsis': 'When a menacing clown wreaks havoc on Gotham City, Batman must accept one of the greatest tests of his ability to fight injustice.',
        'genres': ['Action', 'Crime', 'Drama'],
        'directors': ['Christopher Nolan'],
        'language': 'en',
        'budget': 185000000,
        'revenue': 1004558444,
        'is_featured': True,
    },
    {
        'title': "Schindler's List",
        'release_year': 1993,
        'runtime_minutes': 195,
        'content_rating': 'R',
        'synopsis': 'In German-occupied Poland during World War II, industrialist Oskar Schindler gradually becomes concerned for his Jewish workforce after witnessing their persecution by the Nazis.',
        'genres': ['Biography', 'Drama'],
        'directors': ['Steven Spielberg'],
        'language': 'en',
        'budget': 22000000,
        'revenue': 321306305,
        'is_featured': True,
    },
    {
        'title': 'Pulp Fiction',
        'release_year': 1994,
        'runtime_minutes': 154,
        'content_rating': 'R',
        'synopsis': 'The lives of two mob hitmen, a boxer, a gangster and his wife intertwine in four tales of violence and redemption.',
        'genres': ['Crime', 'Drama'],
        'directors': ['Quentin Tarantino'],
        'language': 'en',
        'budget': 8000000,
        'revenue': 213928762,
    },
    {
        'title': 'Forrest Gump',
        'release_year': 1994,
        'runtime_minutes': 142,
        'content_rating': 'PG-13',
        'synopsis': 'The presidencies of Kennedy and Johnson, the Vietnam War, the Watergate scandal and other historical events unfold from the perspective of an Alabama man with an IQ of 75.',
        'genres': ['Comedy', 'Drama', 'Romance'],
        'directors': ['Steven Spielberg'],
        'language': 'en',
        'budget': 55000000,
        'revenue': 678226133,
        'is_featured': True,
    },
    {
        'title': 'The Godfather',
        'release_year': 1972,
        'runtime_minutes': 175,
        'content_rating': 'R',
        'synopsis': 'The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.',
        'genres': ['Crime', 'Drama'],
        'directors': ['Francis Ford Coppola'],
        'language': 'en',
        'budget': 6000000,
        'revenue': 245066411,
        'is_featured': True,
    },
    {
        'title': 'Goodfellas',
        'release_year': 1990,
        'runtime_minutes': 146,
        'content_rating': 'R',
        'synopsis': 'The story of Henry Hill and his life in the mob, covering his relationship with his wife Karen and his mob partners.',
        'genres': ['Biography', 'Crime', 'Drama'],
        'directors': ['Martin Scorsese'],
        'language': 'en',
        'budget': 25000000,
        'revenue': 46836394,
    },
    {
        'title': 'Interstellar',
        'release_year': 2014,
        'runtime_minutes': 169,
        'content_rating': 'PG-13',
        'synopsis': 'A team of explorers travel through a wormhole in space in an attempt to ensure humanity\'s survival.',
        'genres': ['Adventure', 'Drama', 'Sci-Fi'],
        'directors': ['Christopher Nolan'],
        'language': 'en',
        'budget': 165000000,
        'revenue': 701729206,
        'is_featured': True,
    },
]


class Command(BaseCommand):
    help = 'Seed the database with sample movies data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING('🌱 Seeding database...'))

        # Genres
        self.stdout.write('  Creating genres...')
        genre_map = {}
        for name in GENRES:
            g, created = Genre.objects.get_or_create(name=name, defaults={'slug': slugify(name)})
            genre_map[name] = g
        self.stdout.write(f'  ✅ {len(genre_map)} genres ready')

        # People
        self.stdout.write('  Creating people...')
        person_map = {}
        for p in PEOPLE:
            obj, _ = Person.objects.get_or_create(name=p['name'], defaults={'roles': p['roles']})
            person_map[p['name']] = obj
        self.stdout.write(f'  ✅ {len(person_map)} people ready')

        # Movies
        self.stdout.write('  Creating movies...')
        count = 0
        for m in MOVIES:
            slug = slugify(f"{m['title']}-{m['release_year']}")
            movie, created = Movie.objects.get_or_create(
                slug=slug,
                defaults={
                    'title': m['title'],
                    'synopsis': m['synopsis'],
                    'release_year': m['release_year'],
                    'runtime_minutes': m['runtime_minutes'],
                    'content_rating': m['content_rating'],
                    'language': m['language'],
                    'budget': m.get('budget'),
                    'revenue': m.get('revenue'),
                    'is_featured': m.get('is_featured', False),
                }
            )
            if created:
                for gname in m.get('genres', []):
                    if gname in genre_map:
                        movie.genres.add(genre_map[gname])
                for dname in m.get('directors', []):
                    if dname in person_map:
                        movie.directors.add(person_map[dname])
                count += 1

        self.stdout.write(f'  ✅ {count} new movies created ({len(MOVIES) - count} already existed)')
        self.stdout.write(self.style.SUCCESS('\n✅ Database seeded successfully!'))
        self.stdout.write('   → Run: python manage.py runserver')
        self.stdout.write('   → Docs: http://127.0.0.1:8000/api/docs/')
