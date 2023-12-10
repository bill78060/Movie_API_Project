
from django.shortcuts import render
from django.db.models import Q
from .models import Movie
from django.shortcuts import render, get_object_or_404, redirect
from .forms import MovieForm
import requests

# Create your views here.

def landing_page(request):
    trending_movies = Movie.objects.all().order_by('-id')[:5]  # Fetch the latest 5 movies
    return render(request, 'movies/landing_page.html', {'trending_movies': trending_movies})


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

# Inside views.py
from django.http import JsonResponse

# def search_and_save_movie(request):
#     if request.method == 'POST':
#         # Extract the search query from the form submission
#         search_query = request.POST.get('search_query')

#         # Make an API call to OMDb using the provided fetch_movie_data function
#         movie_data = fetch_movie_data(search_query)

#         # Check if the movie already exists in the database
#         imdb_link = movie_data.get('imdbID')
#         existing_movie_check = check_movie_existence(request, imdb_link)
#         existing_movie_data = existing_movie_check.json()

#         # Return JSON response with the movie_data and existence check
#         return JsonResponse({'movie_data': movie_data, 'exists': existing_movie_data['exists']})

# def search_and_save_movie(request):
#     if request.method == 'POST':
#         # Extract the search query from the form submission
#         search_query = request.POST.get('search_query')

#         # Make an API call to OMDb using the provided fetch_movie_data function
#         movie_data = fetch_movie_data(search_query)

#         # Return JSON response with the movie_data
#         return JsonResponse(movie_data)

def search_and_save_movie(request):
    if request.method == 'POST':
        # Extract the search query from the form submission
        search_query = request.POST.get('search_query')

        # Make an API call to OMDb using the provided fetch_movie_data function
        movie_data = fetch_movie_data(search_query)

        # Return JSON response with the movie_data
        return JsonResponse(movie_data)


# Inside views.py
# Inside views.py
# Inside views.py
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Movie

def save_movie(request):
    if request.method == 'POST':
        # Extract movie details from the form submission
        title = request.POST.get('title')
        director = request.POST.get('director')
        cast = request.POST.get('cast')
        genres = request.POST.get('genres')
        imdb_link = request.POST.get('imdb_link')
        thumbnail_url = request.POST.get('thumbnail_url')

        # Check if the movie already exists in the database
        existing_movie = Movie.objects.filter(title=title).exists()

        if existing_movie:
            # Movie already exists, return a response indicating that
            return JsonResponse({'message': 'Movie already exists in the database'})

        # Save the movie to the database
        Movie.objects.create(
            title=title,
            director=director,
            cast=cast,
            genres=genres,
            imdb_link=imdb_link,
            thumbnail_url=thumbnail_url
        )

        # Return a success response
        return JsonResponse({'message': 'Movie saved successfully'})








# Inside views.py
# Inside views.py


from django.http import JsonResponse
import json

# def search_and_save_movie(request):
#     if request.method == 'POST':
#         # Extract the search query from the form submission
#         search_query = request.POST.get('search_query')

#         # Make an API call to OMDb using the provided fetch_movie_data function
#         movie_data = fetch_movie_data(search_query)

#         # Check if the movie already exists in the database
#         imdb_link = movie_data.get('imdbID')
#         existing_movie_check = check_movie_existence(request, imdb_link)
#         existing_movie_data = json.loads(existing_movie_check.content.decode('utf-8'))

#         # Return JSON response with the movie_data and existence check
#         return JsonResponse({'movie_data': movie_data, 'exists': existing_movie_data['exists']})

# def check_movie_existence(request, imdb_link):
#     existing_movie = Movie.objects.filter(imdb_link=imdb_link).exists()

#     if existing_movie:
#         return JsonResponse({'exists': True, 'message': 'Movie already exists in the database.'})
#     else:
#         return JsonResponse({'exists': False, 'message': 'Movie does not exist in the database.'})
    

# def save_movie(request, movie_data):
#     title = movie_data.get('Title')
#     director = movie_data.get('Director')
#     cast = movie_data.get('Actors')
#     genres = movie_data.get('Genre')
#     imdb_link = movie_data.get('imdbID')
#     thumbnail_url = movie_data.get('Poster')

#     Movie.objects.create(
#         title=title,
#         director=director,
#         cast=cast,
#         genres=genres,
#         imdb_link=imdb_link,
#         thumbnail_url=thumbnail_url
#     )

#     return JsonResponse({'message': 'Movie saved successfully'})

# def search_and_save_movie(request):
#     if request.method == 'POST':
#         search_query = request.POST.get('search_query')
#         movie_data = fetch_movie_data(search_query)
#         imdb_link = movie_data.get('imdbID')

#         existing_movie = Movie.objects.filter(imdb_link=imdb_link).exists()

#         if existing_movie:
#             return JsonResponse({'exists': True, 'message': 'Movie already exists in the database.'})
#         else:
#             save_movie(request, movie_data)
#             return JsonResponse({'exists': False, 'message': 'Movie saved successfully.'})

#     return JsonResponse({'error': 'Invalid request.'})

def fetch_movie_data(title):
    api_key = 'f5845287'  
    url = f'http://www.omdbapi.com/?apikey={api_key}&t={title}'
    response = requests.get(url)
    return response.json()

# views.py
