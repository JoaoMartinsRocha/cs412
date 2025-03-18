# File: admin.py
# Author: João Pedro Rocha (jprocha@bu.edu), 02/18/2025
# Description: This file registers the models created in models.py with the django admin

from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Profile)
admin.site.register(StatusMessage)
admin.site.register(Image)
admin.site.register(StatusImage)
admin.site.register(Friend)