# File: models.py
# Author: João Pedro Rocha (jprocha@bu.edu), 02/18/2025
# Description: models file used to create the profile model used in the mini_fb application 


from django.db import models

# Create your models here.

class Profile(models.Model):
    '''Encapsulate the idea of an Article by some author.'''

    # data attributes of the profile model:
    first_name = models.TextField(blank=True)
    last_name = models.TextField(blank=True)
    city = models.TextField(blank=True)
    email = models.TextField(blank=True)
    profile_image_url = models.URLField(blank=True)
    
    def __str__(self):
        '''Return a string representation of this Article object.'''
        return f'{self.first_name} {self.last_name}\'s profile'
    
    def get_all_status_messages(self):
        '''Return all of the comments about this article.'''
        comments = StatusMessage.objects.filter(profile=self)
        return comments
    

class StatusMessage(models.Model):
    '''Encapsulate the idea of an Article by some author.'''

    # data attributes of the StatusMessage model:

    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    message = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now=True)
    
    
    
    def __str__(self):
        '''Return a string representation of this Article object.'''
        return f'{self.message}'