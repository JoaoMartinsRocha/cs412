# File: urls.py
# Author: João Pedro Rocha (jprocha@bu.edu), 04/15/2025
# Description: urls file for project app, recieves http requests and routes them to correct function within views.py.  

from django.urls import path
from django.conf import settings
from .views import *
from django.contrib.auth import views as auth_views 
from . import views

urlpatterns = [ 
    path('pokemon_species', ShowAllPokemonSpeciesView.as_view(), name='show_all_species'),
    path('trainers', ShowAllTrainersView.as_view(), name='show_all_trainers'),
    
    path('moves', ShowAllMovesView.as_view(), name='show_all_moves'),
    path('move/<int:pk>/delete', DeleteMoveView.as_view(), name='delete_move'),

    path('pokemon_species/<int:pk>', ShowPokemonSpeciesView.as_view(), name='show_species'),
    path('pokemon_species/<int:pk>/update', UpdatePokemonSpeciesView.as_view(), name='update_species'),
    
    path('trainer/<int:pk>', ShowTrainerView.as_view(), name='show_trainer'),
    path('trainer/<int:pk>/update', UpdateTrainerView.as_view(), name='update_trainer'),
    path('trainer/<int:pk>/catch', CatchPokemonView.as_view(), name='catch'),
    path('trainer/<int:pk>/catch/<int:pk1>', CreateCaughtPokemonView.as_view(), name='create_caught'),

    path('move/<int:pk>', ShowMoveDescriptionView.as_view(), name='show_move_description'),
    
    path('trainer/<int:pk>/box', ShowTrainerBoxView.as_view(), name='show_box'),
    path('caught_pokemon/<int:pk>', ShowCaughtPokemonView.as_view(), name='show_caught'),

    path('toggle_in_team/<int:pk>', ToggleInTeamView.as_view(), name="toggle_in_team"),


    # path('profile/create_status', CreateStatusMessageView.as_view(), name='create_status'),
    # path('profile/update', UpdateProfileView.as_view(), name='update_profile'),
    # path('profile/add_friend/<int:other_pk>', AddFriendView.as_view(), name='add_friend'),
    # path('profile/friend_suggestions', ShowFriendsSuggestionsView.as_view(), name='show_friend_suggestions'),
    # path('profile/news_feed', ShowNewsFeedView.as_view(), name='show_news_feed'),

    
    # path('status/<int:pk>/update', UpdateStatusMessageView.as_view(), name='update_status'),
    path('create_trainer', CreateTrainerView.as_view(), name='create_trainer'),
    path('create_pokemon_species', CreatePokemonSpeciesView.as_view(), name='create_species'),
    path('create_move', CreateMoveView.as_view(), name='create_move'),

    # path('login/', auth_views.LoginView.as_view(template_name='mini_fb/login.html'), name='login'), ## NEW
	# path('logout/', auth_views.LogoutView.as_view(template_name='mini_fb/logged_out.html'), name='logout'), ## NEW
    # path('register/', RegistrationView.as_view(), name='register'),

]