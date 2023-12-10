# movies/urls.py
from django.urls import path
from . import views

urlpatterns = [

    path('', views.landing_page, name='landing_page'),
    path('movies/', views.movie_list, name='movie_list'),
    path('add/', views.movie_add, name='movie_add'),
    path('<int:pk>/', views.movie_detail, name='movie_detail'),
    path('<int:pk>/edit/', views.movie_edit, name='movie_edit'),
    path('search/', views.movie_search, name='movie_search'),

    path('movies/edit/', views.edit_movie_list, name='edit_movie_list'),
    path('movies/<int:pk>/edit/', views.movie_edit, name='movie_edit'),
    path('movies/<int:pk>/delete/', views.movie_delete, name='movie_delete'),

    path('search_and_save_movie/', views.search_and_save_movie, name='search_and_save_movie'),
    path('save_movie/', views.save_movie, name='save_movie'),
    # path('check_movie_existence/<str:imdb_link>/', views.check_movie_existence, name='check_movie_existence'), 
]
