# File: admin.py
# Author: João Pedro Rocha (jprocha@bu.edu), 02/18/2025
# Description: This file registers the profile model created in models.py with the django admin

from django.contrib import admin

# Register your models here.
from .models import Profile
admin.site.register(Profile)