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
        messages = StatusMessage.objects.filter(profile=self)
        return messages
    def get_friends(self):
        '''Return all friends of this profile'''
        id1 = Friend.objects.filter(profile1=self).values_list('profile2', flat=True)
        id2 = Friend.objects.filter(profile2=self).values_list('profile1', flat=True)
        friends1 = Profile.objects.filter(id__in=id1)
        friends2 = Profile.objects.filter(id__in=id2)

        return list(friends1) + list(friends2)
    
    def get_friend_suggestions(self):
        '''Method to get freind suggestions for a profile'''
        suggestions = []
        friend_list = self.get_friends()
        for friend in friend_list:
            friends_of_friend = friend.get_friends()
        
            for ff in friends_of_friend:

                if(self.pk != ff.pk and not Friend.objects.filter(profile1=self, profile2=ff).exists() and not Friend.objects.filter(profile1=ff, profile2=self).exists() and ff not in suggestions):
                    suggestions += [ff] 

        return suggestions
    
    def add_friend(self, other):
        '''Method to create and save a freind object'''

        if(self.pk == other.pk):
            return 
        elif(Friend.objects.filter(profile1=self, profile2=other).exists() or Friend.objects.filter(profile1=other, profile2=self).exists()):
            return
        # Check if friend pair already exists
        new_freind = Friend()
        new_freind.profile1 = self
        new_freind.profile2 = other

        new_freind.save()

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

class Friend(models.Model): # Models a reltionship set between Image and Status Message, Many to many

    profile1 = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name='profile1') # foreign key
    profile2 = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name='profile2') # foreign key
    timestamp = models.DateTimeField(auto_now=True) # when it was created

    def __str__(self):
        '''Return a string representation of this Article object.'''
        return f'{self.profile1.first_name} & {self.profile2.first_name}'








