# File: views.py
# Author: João Pedro Rocha (jprocha@bu.edu), 02/18/2025
# Description: Views file for mini_fb app, recieves http requests and responds with correct html template. 
# Two views include either showing all the profiles or only one specific profile. Views also handle creating new prfolies and new status messages, and registering any related images 
# They are also capable of updating/deleting a profile's or a status message


from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import *
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm, UpdateStatusMessageForm
from django.urls import reverse
from django.shortcuts import redirect

from django.contrib.auth.mixins import LoginRequiredMixin ## NEW

from django.contrib.auth.forms import UserCreationForm ## NEW
from django.contrib.auth.models import User


class ShowAllProfilesView(ListView):
    '''Display all prfiles'''
    model = Profile
    template_name = "mini_fb/show_all_profiles.html"
    context_object_name = "profiles"

    def get_context_data(self, **kwargs):
        '''Return the dictionary of context variables for use in the template.'''
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            logged_in_user = self.request.user
            profile = Profile.objects.filter(user=logged_in_user)[0]
        else:
            logged_in_user = None
            profile = None


        # add this article into the context dictionary:
        context['logged_profile'] = profile
        return context


    # might need to make a get context object data
class CustomLoginRequiredMixin(LoginRequiredMixin):
    
    # def get_object(self):
        
    #     if self.request.user.is_authenticated:
    #         logged_in_user = self.request.user
    #         profile = Profile.objects.filter(user=logged_in_user)[0]
    #     else:
    #         profile = None
        
    #     return profile
    
    
    def get_context_data(self):
        '''Return the dictionary of context variables for use in the template.'''
        context = super().get_context_data()
        if self.request.user.is_authenticated:
            logged_in_user = self.request.user
            profile = Profile.objects.filter(user=logged_in_user)[0]
        else:
            logged_in_user = None
            profile = None


        # add this article into the context dictionary:
        context['logged_profile'] = profile
        return context        


class ShowProfilePageView(DetailView):
    '''Display a singe Profile'''

    model = Profile
    template_name = "mini_fb/show_profile.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        '''Return the dictionary of context variables for use in the template.'''
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            logged_in_user = self.request.user
            profile = Profile.objects.filter(user=logged_in_user)[0]
        else:
            logged_in_user = None
            profile = None


        # add this article into the context dictionary:
        context['logged_profile'] = profile
        return context


class ShowFriendsSuggestionsView(LoginRequiredMixin, DetailView):
    '''View for showing friend suggestions page'''

    model = Profile
    template_name = "mini_fb/friend_suggestions.html"
    context_object_name = "profile"

    def get_object(self):
        
        if self.request.user.is_authenticated:
            logged_in_user = self.request.user
            profile = Profile.objects.filter(user=logged_in_user)[0]
        else:
            profile = None
        
        return profile
    
    def get_context_data(self, **kwargs):
        '''Return the dictionary of context variables for use in the template.'''
        context = super().get_context_data()
        if self.request.user.is_authenticated:
            logged_in_user = self.request.user
            profile = Profile.objects.filter(user=logged_in_user)[0]
        else:
            logged_in_user = None
            profile = None


        # add this article into the context dictionary:
        # context['profile'] = profile
        context['logged_profile'] = profile
        return context        

    



class ShowNewsFeedView(LoginRequiredMixin, DetailView):
    '''View for showing news feed'''

    model = Profile
    template_name = "mini_fb/news_feed.html"
    context_object_name = "profile"

    def get_object(self):
        
        if self.request.user.is_authenticated:
            logged_in_user = self.request.user
            profile = Profile.objects.filter(user=logged_in_user)[0]
        else:
            profile = None
        
        return profile
    
    def get_context_data(self, **kwargs):
        '''Return the dictionary of context variables for use in the template.'''
        context = super().get_context_data()
        if self.request.user.is_authenticated:
            logged_in_user = self.request.user
            profile = Profile.objects.filter(user=logged_in_user)[0]
        else:
            logged_in_user = None
            profile = None


        # add this article into the context dictionary:
        # context['profile'] = profile
        context['logged_profile'] = profile
        return context        


class CreateProfileView(CreateView):
    '''A view to handle creation of a new Profile.
    (1) display the HTML form to user (GET)
    (2) process the form submission and store the new Profile object (POST)
    '''

    form_class = CreateProfileForm
    template_name = "mini_fb/create_profile_form.html"


class CreateStatusMessageView(CustomLoginRequiredMixin, CreateView):
    '''A view to handle creation of a new Status Message.
    (1) display the HTML form to user (GET)
    (2) process the form submission and store the new Status Message object (POST)
    '''

    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_form.html"

    def get_success_url(self):
        '''Return the URL to redirect to after successfully submitting form.'''
        # return reverse('show_all')
        ## note: this is not ideal, because we are redirected to the main page.
        pk = Profile.objects.filter(user=self.request.user)[0].pk
        return reverse('show_profile', kwargs={'pk':pk})
    
    def get_context_data(self):
        '''Return the dictionary of context variables for use in the template.'''

        # calling the superclass method
        context = super().get_context_data()

        # find/add the article to the context data
        # retrieve the PK from the URL pattern
        pk = Profile.objects.filter(user=self.request.user)[0].pk
        profile = Profile.objects.get(pk=pk)

        # add this article into the context dictionary:
        context['profile'] = profile
        return context

    def form_valid(self, form):
        '''This method handles the form submission and saves the 
        new object to the Django database.
        We need to add the foreign key (of the Profile) to the status message
        object before saving it to the database.
        We also have to register any new images if they were uploaded
        '''
        
		# instrument our code to display form fields: 
        print(f"CreateStatusMessageView.form_valid: form.cleaned_data={form.cleaned_data}")
        
        # retrieve the PK from the URL pattern
        pk = Profile.objects.filter(user=self.request.user)[0].pk
        profile = Profile.objects.get(pk=pk)
        # attach this article to the comment
        form.instance.profile = profile # set the FK

        # save the status message to database
        sm = form.save() # Note that the variable sm is a reference to the new StatusMessage object.

        # read the file from the form:
        files = self.request.FILES.getlist('files')
        print(files)

        # For each image, create a new image and matching status image object
        for file in files:

            new_image = Image()
            print(new_image)
            new_image.profile = profile  # Attach profile foriegn key to image
            new_image.image_file = file # Attach iage file to image
            new_image.save() # Save the image

            # register relationship between image and status messsage by creating a status image
            new_status_image = StatusImage()
            new_status_image.image = new_image 
            new_status_image.status_message = sm 
            new_status_image.save()
            

        # delegate the work to the superclass method form_valid:
        return super().form_valid(form)

class UpdateProfileView(CustomLoginRequiredMixin, UpdateView):
    '''View Handles updating a profile, responds to GET and POST requests differently'''

    model = Profile
    form_class = UpdateProfileForm 
    template_name = "mini_fb/update_profile_form.html"

    def get_object(self):
        
        if self.request.user.is_authenticated:
            logged_in_user = self.request.user
            profile = Profile.objects.filter(user=logged_in_user)[0]
        else:
            profile = None
        
        return profile

class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):


    model = StatusMessage
    template_name = "mini_fb/delete_status_form.html"
    context_object_name = 'status_message'

    def get_context_data(self, **kwargs):
        '''Return the dictionary of context variables for use in the template.'''
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            logged_in_user = self.request.user
            profile = Profile.objects.filter(user=logged_in_user)[0]
        else:
            logged_in_user = None
            profile = None


        # add this article into the context dictionary:
        context['logged_profile'] = profile
        return context


    def get_success_url(self):
        '''Return the URL to redirect to after successfully submitting form.'''
        
        ## Find pk of comment first
        pk = self.kwargs['pk']
        # Find  the comment object
        status_message = StatusMessage.objects.get(pk=pk)

        profile = status_message.profile

        return reverse('show_profile', kwargs={'pk': profile.pk})
    

    
    

class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
    '''View Handles updating a profile, responds to GET and POST requests differently'''

    model = StatusMessage
    form_class = UpdateStatusMessageForm 
    template_name = "mini_fb/update_status_form.html"

    def get_context_data(self, **kwargs):
        '''Return the dictionary of context variables for use in the template.'''
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            logged_in_user = self.request.user
            profile = Profile.objects.filter(user=logged_in_user)[0]
        else:
            logged_in_user = None
            profile = None


        # add this article into the context dictionary:
        context['logged_profile'] = profile
        return context


    def get_success_url(self):
        '''Return the URL to redirect to after successfully submitting form.'''
        
        ## Find pk of comment first
        pk = self.kwargs['pk']
        # Find  the comment object
        status_message = StatusMessage.objects.get(pk=pk)

        profile = status_message.profile

        return reverse('show_profile', kwargs={'pk': profile.pk})
    

class AddFriendView(CustomLoginRequiredMixin, View):
    '''This view handles creating a freind relationship between to profiles'''

    def dispatch(self, request, *args, **kwargs):
        # pk = self.kwargs['pk']
        pk_other = self.kwargs['other_pk']

        p1 = Profile.objects.filter(user=self.request.user)[0]
        p2 = Profile.objects.get(pk=pk_other)
        p1.add_friend(p2)

        return  super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        """Handles GET requests"""
        return redirect(self.get_success_url())
        
        
    def get_success_url(self):

        ## Find pk of profile
        pk = Profile.objects.filter(user=self.request.user)[0].pk
        return reverse('show_profile', kwargs={'pk':pk})

    
    

