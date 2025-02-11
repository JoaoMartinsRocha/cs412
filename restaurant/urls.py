# File: urls.py
# Author: João Pedro Rocha (jprocha@bu.edu), 02/11/2025
# Description: urls file for restaurant app, recieves http requests and routes them to correct function within views.py. 


from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [ 
    # path(r'', views.home, name="home"),
    path(r'', views.main, name="main_empty"),
    path(r'main', views.main, name="main"),
    path(r'order', views.order, name="order"),
    path(r'confirmation', views.confirmation, name="confirmation"),
]