# File: models.py
# Author: João Pedro Rocha (jprocha@bu.edu), 02/18/2025
# Description: models file used to create the profile model and the Status Message model used in the mini_fb application 


from django.db import models
from django.urls import reverse

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
    
    def get_absolute_url(self):
        '''Return the URL to display one instance of this model.'''
        return reverse('show_profile', kwargs={'pk': self.pk})
    
    def get_all_status_messages(self):
        '''Return all of the comments about this article.'''
        comments = StatusMessage.objects.filter(profile=self)
        return comments
    

class StatusMessage(models.Model):
    '''Encapsulates the idea of a Status message by some profile.'''

    # data attributes of the StatusMessage model:

    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    message = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now=True)
    
    def get_images(self):
        '''Return all of the comments about this article.'''
        status_image_set = StatusImage.objects.filter(status_message=self)
        return status_image_set  # Now you can loop through these and
    
    def __str__(self):
        '''Return a string representation of this Article object.'''
        return f'{self.message}'

class Image(models.Model):
    '''Encapsulates the idea of an Image related to some profile.'''

    profile = models.ForeignKey("Profile", on_delete=models.CASCADE) # foreign key
    image_file = models.ImageField(blank=True) # In the media directory

    timestamp = models.DateTimeField(auto_now=True) # when it was created
    caption = models.TextField(blank=True)

class StatusImage(models.Model): # Models a reltionship set between Image and Status Message, Many to many

    image = models.ForeignKey("Image", on_delete=models.CASCADE) # foreign key
    status_message = models.ForeignKey("StatusMessage", on_delete=models.CASCADE) # foreign key





