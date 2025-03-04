# File: forms.py
# Author: João Pedro Rocha (jprocha@bu.edu), 02/25/2025
# Description: forms file used to create the form classes used by the CreateView methods in the views.py file

from django import forms
from .models import Profile, StatusMessage


class CreateProfileForm(forms.ModelForm):
    '''A form to add an Article to the database.'''

    class Meta:
        '''associate this form with a model from our database.'''
        model = Profile
        fields = ['first_name', 'last_name', 'city', 'email', 'profile_image_url']


class CreateStatusMessageForm(forms.ModelForm):
    '''A form to add an Article to the database.'''

    class Meta:
        '''associate this form with a model from our database.'''
        model = StatusMessage
        fields = ['message']

class UpdateProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['city', 'email', 'profile_image_url']


class UpdateStatusMessageForm(forms.ModelForm):

    class Meta:
        model = StatusMessage
        fields = ['message']