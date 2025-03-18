# File: urls.py
# Author: João Pedro Rocha (jprocha@bu.edu), 02/18/2025
# Description: urls file for mini_fb app, recieves http requests and routes them to correct function within views.py. Also handles routing for specific profiles based on primary key  

from django.urls import path
from django.conf import settings
from .views import *

urlpatterns = [ 
    path('', ShowAllProfilesView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>', ShowProfilePageView.as_view(), name='show_profile'),
    path('profile/<int:pk>/create_status', CreateStatusMessageView.as_view(), name='create_status'),
    path('profile/<int:pk>/update', UpdateProfileView.as_view(), name='update_profile'),
    path('profile/<int:pk>/add_friend/<int:other_pk>', AddFriendView.as_view(), name='add_friend'),
    path('profile/<int:pk>/friend_suggestions', ShowFriendsSuggestionsView.as_view(), name='show_friend_suggestions'),

    path('status/<int:pk>/delete', DeleteStatusMessageView.as_view(), name='delete_status'),
    path('status/<int:pk>/update', UpdateStatusMessageView.as_view(), name='update_status'),
    path('create_profile', CreateProfileView.as_view(), name='create_profile'),

]