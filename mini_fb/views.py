# File: views.py
# Author: João Pedro Rocha (jprocha@bu.edu), 02/18/2025
# Description: Views file for mini_fb app, recieves http requests and responds with correct html template. 
# Two views include either showing all the profiles or only one specific profile. 


from django.shortcuts import render
from django.views.generic import ListView, DetailView
from.models import Profile


class ShowAllProfilesView(ListView):

    model = Profile
    template_name = "mini_fb/show_all_profiles.html"
    context_object_name = "profiles"


class ShowProfilePageView(DetailView):
    '''Display a singe Article'''

    model = Profile
    template_name = "mini_fb/show_profile.html"
    context_object_name = "profile"