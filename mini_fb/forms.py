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