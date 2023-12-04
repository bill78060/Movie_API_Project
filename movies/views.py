
from django.shortcuts import render
from django.db.models import Q
from .models import Movie
from django.shortcuts import render, get_object_or_404, redirect
from .forms import MovieForm
import requests

# Create your views here.

# movies/views.py

def landing_page(request):
    return render(request, 'movies/landing_page.html')


def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'movies/movie_list.html', {'movies': movies})

def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    return render(request, 'movies/movie_detail.html', {'movie': movie})

def movie_add(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            movie_title = form.cleaned_data['title']
            movie_data = fetch_movie_data(movie_title)
            if movie_data.get('Response') == 'True':
                form.instance.thumbnail_url = movie_data.get('Poster')
                form.instance.imdb_link = f"https://www.imdb.com/title/{movie_data.get('imdbID')}/"
            form.save()
            return redirect('movie_list')
    else:
        form = MovieForm()
    return render(request, 'movies/movie_form.html', {'form': form})

def edit_movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'movies/edit_movie_list.html', {'movies': movies})

def movie_edit(request, pk):
    movie = get_object_or_404(Movie, pk=pk)

    if request.method == 'POST':
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            movie_title = form.cleaned_data['title']
            movie_data = fetch_movie_data(movie_title)
            if movie_data.get('Response') == 'True':
                form.instance.thumbnail_url = movie_data.get('Poster')
                form.instance.imdb_link = f"https://www.imdb.com/title/{movie_data.get('imdbID')}/"
            form.save()
            return redirect('edit_movie_list')
    else:
        form = MovieForm(instance=movie)

    return render(request, 'movies/movie_edit.html', {'form': form, 'movie': movie})

def movie_delete(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    movie.delete()
    return redirect('edit_movie_list')


def fetch_movie_data(title):
    api_key = 'f5845287'  
    url = f'http://www.omdbapi.com/?apikey={api_key}&t={title}'
    response = requests.get(url)
    return response.json()

def fetch_movie_poster(imdb_id):
    api_key = 'f5845287'  
    url = f'http://img.omdbapi.com/?apikey={api_key}&i={imdb_id}'
    response = requests.get(url)
    return response.content


def movie_search(request):
    query = request.GET.get('query')
    search_by = request.GET.get('search_by', 'all')

    if query:
        if search_by == 'director':
            movies_local = Movie.objects.filter(director__icontains=query)
        elif search_by == 'cast':
            movies_local = Movie.objects.filter(cast__icontains=query)
        elif search_by == 'genres':
            movies_local = Movie.objects.filter(genres__icontains=query)
        elif search_by == 'title':
            movies_local = Movie.objects.filter(title__icontains=query)
        else:
            movies_local = Movie.objects.filter(
                Q(title__icontains=query) |
                Q(director__icontains=query) |
                Q(cast__icontains=query) |
                Q(genres__icontains=query)
            )
    else:
        # Handle the case when the search query is empty
        movies_local = Movie.objects.none()

    return render(request, 'movies/movie_search.html', {'movies': movies_local, 'query': query, 'search_by': search_by})
