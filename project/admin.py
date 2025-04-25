# File: admin.py
# Author: João Pedro Rocha (jprocha@bu.edu), 04/15/2025
# Description: This file registers the models created in models.py with the django admin

from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Trainer)
admin.site.register(Pokemon_Species)
admin.site.register(Move)
admin.site.register(HasCaughtPokemon)
