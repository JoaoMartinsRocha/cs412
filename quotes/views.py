from django.shortcuts import render

# Create your views here.
# Create your views here.
import time 
import random

quotes = ["I am Iron Man", "Genius, billionaire, playboy, philanthropist", "If we can't protect the world, then you can be damn sure we'll avenge it"]
images = ["images/Tony1.avif", "images/Tony2.avif", "images/Tony3.jpg"]

def quote(request):
    ''' Respond to the URL '', delegate work to tempate.'''
    '''Define a view to show the 'home.html' template.'''
    
	# the template to which we will delegate the work
    template = 'quotes/quote.html'

    len_quotes = len(quotes)
    len_images = len(images)

    context = {
        'quote' : quotes[random.randint(0,len_quotes - 1)],
        'image' : images[random.randint(0,len_images - 1)],
    }

    return render(request, template, context)

def show_all(request):
    
    template = 'quotes/show_all.html'

    context = {
        'quotes' : quotes,
        'images' : images,
    }

    return render(request, template, context)

def about(request):
    ''' Respond to the URL 'about', delegate work to tempate.'''
    '''Define a view to show the 'home.html' template.'''
    
	# the template to which we will delegate the work
    template = 'quotes/about.html'


    return render(request, template)