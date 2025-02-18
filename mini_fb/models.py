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