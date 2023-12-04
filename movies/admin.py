from django.contrib import admin
from .models import Movie

# Register your models here.

# movies/admin.py

class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'director')  
    search_fields = ('title', 'director', 'cast', 'genres') 

admin.site.register(Movie, MovieAdmin)
