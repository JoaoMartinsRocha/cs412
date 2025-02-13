# File: views.py
# Author: João Pedro Rocha (jprocha@bu.edu), 02/11/2025
# Description: Views file for restaurant app, recieves http requests and responds with correct html template. 
# Also handles logic for context variables passed to templates. It adds up the total cost of an order, and also generates a random special of the day. 
 
from django.shortcuts import render


import time 
import random

daily_specials = ["RedSox Burger", "The Harvard Special", "Celtics Sandwich"] # Possible daily specials
regular = ["Burger", "Cheese Burger", "Fries", "Add cheese"] # Possible regular orders
prices = { # prices for orders
    "Burger": 2,
    "Cheese Burger": 3,
    "Fries": 2,
    "Add cheese": 1,
    "special": 5,
}

def main(request):
    ''' Respond to the URL '' and 'main', delegate work to tempate.'''
    
	# the template to which we will delegate the work
    template = 'restaurant/main.html'

    
    context = {
        'image' : "restaurant/images/Burger.jpg",
    }

    return render(request, template, context)

def order(request):
    ''' Respond to the URL 'order', delegate work to tempate.'''
    
    template = 'restaurant/order.html'
    len_special= len(daily_specials)
    context = {
        'special' : daily_specials[random.randint(0,len_special - 1)], # Calculates random index from speical orders array 
    }

    return render(request, template, context)

def confirmation(request):
    ''' Respond to the URL 'confirmation', processes form and sends values to template.'''
    

    context = {
            "regulars": [],
            "special": "",
            "special_instructions": "",
            "readytime" : "" 
        }
    
    print(request.POST)
    template = 'restaurant/confirmation.html'
    # read the form data into python variables:
    if request.POST:

        total = 0

        # First loop through the keys in the request
        for key in request.POST:
            if request.POST[key] != "" and key != "csrfmiddlewaretoken": # If the value is empty or its the csrf token don't do anything
                if key in regular: # If the key is in the array containing the names of the regular orders add it to the context variables
                    context["regulars"] += [request.POST[key]]
                    total += prices[key] # accumulate total
                elif key == "special": # If the key is the specials key than add that to the right place in the context dictionary
                    context["special"] = request.POST[key]
                    total += prices[key]
                else: # Else it's another field
                    context.update({key: request.POST[key]})
            

        context.update({"total": total}) # add total

        # Get random time 
        ctime_seconds = time.time()
        seconds = random.randint(1800, 3600)
        readytime_seconds = ctime_seconds + seconds
        ready_time = time.ctime(readytime_seconds)
        context.update({"readytime": ready_time})


        print("Total is: " + str(total))
        print(context)

    return render(request, template, context=context)
