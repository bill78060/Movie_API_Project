from django.db import models

# Create your models here.

# movies/models.py
from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=255)
    director = models.CharField(max_length=255)
    cast = models.TextField()
    genres = models.TextField()
    imdb_link = models.URLField()
    thumbnail_url = models.URLField()

    def __str__(self):
        return self.title

