# File: urls.py
# Author: João Pedro Rocha (jprocha@bu.edu), 02/18/2025
# Description: urls file for mini_fb app, recieves http requests and routes them to correct function within views.py. Also handles routing for specific profiles based on primary key  

from django.urls import path
from django.conf import settings
from .views import *
from django.contrib.auth import views as auth_views 

urlpatterns = [ 
    path('', ShowAllProfilesView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>', ShowProfilePageView.as_view(), name='show_profile'),
    path('profile/create_status', CreateStatusMessageView.as_view(), name='create_status'),
    path('profile/update', UpdateProfileView.as_view(), name='update_profile'),
    path('profile/add_friend/<int:other_pk>', AddFriendView.as_view(), name='add_friend'),
    path('profile/friend_suggestions', ShowFriendsSuggestionsView.as_view(), name='show_friend_suggestions'),
    path('profile/news_feed', ShowNewsFeedView.as_view(), name='show_news_feed'),

    path('status/<int:pk>/delete', DeleteStatusMessageView.as_view(), name='delete_status'),
    path('status/<int:pk>/update', UpdateStatusMessageView.as_view(), name='update_status'),
    path('create_profile', CreateProfileView.as_view(), name='create_profile'),

    path('login/', auth_views.LoginView.as_view(template_name='mini_fb/login.html'), name='login'), ## NEW
	path('logout/', auth_views.LogoutView.as_view(template_name='mini_fb/logged_out.html'), name='logout'), ## NEW
    # path('register/', RegistrationView.as_view(), name='register'),

]