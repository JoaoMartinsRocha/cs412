# File: forms.py
# Author: João Pedro Rocha (jprocha@bu.edu), 04/19/2025
# Description: forms file used to create the form classes used by the CreateView and UpdateView generic classes in the views.py file


from django import forms
from .models import Trainer, Pokemon_Species, Move, HasCaughtPokemon
from django.core.exceptions import ValidationError


class CreateTrainerForm(forms.ModelForm):
    '''A form to add a trainer to the database.'''

    class Meta:
        '''associate this form with a model from our database.'''
        model = Trainer
        fields = ['first_name', 'last_name', 'pokemon_region', 'pokemon_town', 'trainer_image_url', 'rival']


class UpdateTrainerForm(forms.ModelForm):

    class Meta:
        model = Trainer
        fields = ['pokemon_region', 'pokemon_town', 'trainer_image_url']

class CreatePokemonSpeciesForm(forms.ModelForm):
    '''A form to add a pokemon species to the database.'''

    class Meta:
        '''associate this form with a model from our database.'''
        model = Pokemon_Species
        fields = '__all__'

class UpdatePokemonSpeciesForm(forms.ModelForm):
    '''A form to add a pokemon species to the database.'''

    class Meta:
        '''associate this form with a model from our database.'''
        model = Pokemon_Species
        fields = ['pokemon_image_url', 'move1', 'move2', 'move3', 'move4']

class CreateMoveForm(forms.ModelForm):
    '''A form to add a pokemon species to the database.'''

    class Meta:
        '''associate this form with a model from our database.'''
        model = Move
        fields = '__all__'


class CreateCaughtPokemonForm(forms.ModelForm):
    '''A form to add a pokemon species to the database.'''

    class Meta:
        '''associate this form with a model from our database.'''
        model = HasCaughtPokemon
        exclude = ['trainer', 'species']

    