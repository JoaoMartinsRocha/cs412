# File: urls.py
# Author: João Pedro Rocha (jprocha@bu.edu), 02/04/2025
# Description: urls file for quotes app, recieves http requests and routes them to correct function within views.py. 


from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [ 
    # path(r'', views.home, name="home"),
    path(r'', views.quote, name="quote_empty"),
    path(r'quote', views.quote, name="quote"),
    path(r'show_all', views.show_all, name="show_all_page"),
    path(r'about', views.about, name="about_page"),
]