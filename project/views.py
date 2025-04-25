# File: views.py
# Author: João Pedro Rocha (jprocha@bu.edu), 04/15/2025
# Description: Views file for project app, recieves http requests and responds with correct html template.
# This file is responsible for processing and responding to incoming http requests from the urls.py file
# Uses generic view classes to coordinate CRUD operations, classes include: ListView, DetailView, CreateView, UpdateView, DeleteView and just View  to do so


from django.shortcuts import render

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import *
from .forms import *
from django.urls import reverse
from django.shortcuts import redirect

from django.contrib.auth.mixins import LoginRequiredMixin 

from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User
from django.forms import ValidationError
from collections import Counter

import plotly
import plotly.graph_objs as go


class ShowAllPokemonSpeciesView(ListView):
    '''Display all pokemon species'''
    model = Pokemon_Species
    template_name = "project/show_all_species.html"
    context_object_name = "species"


   

class CatchPokemonView(ListView):
    '''Display all pokemon species, also allowing a trainer to catch them'''
    model = Pokemon_Species
    template_name = "project/show_all_speciesToCatch.html"
    context_object_name = "species"

    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        pk = self.kwargs['pk']
        trainer = Trainer.objects.get(pk=pk)

        data['t'] = trainer
        return data


class ShowAllTrainersView(ListView):
    '''Display all trainers'''
    model = Trainer
    template_name = "project/show_all_trainers.html"
    context_object_name = "trainers"


    

class ShowAllMovesView(ListView):
    '''Display all moves'''
    model = Move
    template_name = "project/show_all_moves.html"
    context_object_name = "moves"


  

class ShowPokemonSpeciesView(DetailView):
    '''Display a singe Pokemon species'''

    model = Pokemon_Species
    template_name = "project/show_species.html"
    context_object_name = "species"



class ShowTrainerView(DetailView):
    '''Display a singe Trainer'''

    model = Trainer
    template_name = "project/show_trainer.html"
    context_object_name = "trainer"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        
        pk = self.kwargs['pk']
        trainer = Trainer.objects.get(pk=pk)
        all_caught = trainer.get_caught_pokemon()
    
        in_team = all_caught.filter(in_team=True)
       
        data['team'] = in_team

        return data

class ShowMoveDescriptionView(DetailView):
    '''Display the description for a move'''

    model = Move
    template_name = "project/show_move_description.html"
    context_object_name = "move"


class ShowTrainerBoxView(DetailView):
    '''Display the Trainers pc box'''

    model = Trainer
    template_name = "project/show_box.html"
    context_object_name = "trainer"

    def get_context_data(self, **kwargs):
        ''' This method filters out all the pokemon that are currently in our team
            It also processes the a form subission and filters out box pokemon based on the results
            and it creates 3 graphs summarizing the data of the caught pokemon
        '''
        data = super().get_context_data(**kwargs)
        trainer = Trainer.objects.get(pk=self.kwargs['pk'])

        caught_pokemon = trainer.get_caught_pokemon()

        # If all pokemon are in the team and none are in the box
        if(trainer.all_pokemon_in_team()):
            data['box_pokemon'] = HasCaughtPokemon.objects.none()
        else: 
            caught_pokemon = caught_pokemon.filter(in_team=False)
            data['box_pokemon'] = caught_pokemon
                
        # Filter this based on search --> self.request.GET
        data['box_pokemon'] = search(self.request.GET, data['box_pokemon'])

        # Begin graph creation for distibution of levels across the boxed pokemon

        min_level = 1
        max_level = 101
        if 'min_level' in self.request.GET:
            min_l = int(self.request.GET['min_level'])
            if min_l:
                min_level = min_l
        
        if 'max_level' in self.request.GET:
            max_l= int(self.request.GET['max_level'])
            if max_l:
                max_level = max_l + 1

        # Full level range for Gen 1 (1–100) in steps of 10
        levels = list(range(min_level, max_level, 10))

        counts = []
        labels = []

        for i in levels:
            lower = i
            upper = i + 9  # inclusive upper range
            

            # Filter levels in [i, i+9]
            bucket = data['box_pokemon'].filter(level__gte=lower, level__lte=upper)
            counts.append(bucket.count())

            labels.append(f"{lower}-{upper}")

        fig = go.Bar(x=labels, y=counts)
        title_text = f"Level distribution (n={len(data['box_pokemon'])})"
        graph_div_level_dist = plotly.offline.plot({"data": [fig], 
                                         "layout_title_text": title_text,
                                         }, auto_open=False, output_type="div",
                                         
                                         ) 
        data['graph_div_level_dist'] = graph_div_level_dist

        # Begin creation of average stats across boxed pokemon

        stats = ["hit points", "attack", "special", "defense", "accuracy", "evasiveness", "speed"]
        stat_totals = [0, 0, 0, 0, 0, 0, 0]
        for p in data['box_pokemon']:
            stat_totals[0] += p.hit_points
            stat_totals[1] += p.attack
            stat_totals[2] += p.special
            stat_totals[3] += p.defense
            stat_totals[4] += p.accuracy
            stat_totals[5] += p.evasiveness
            stat_totals[6] += p.speed
        
        if(len(data['box_pokemon'])):
            stat_avg = [(v/len(data['box_pokemon'])) for v in stat_totals]
        else:
            stat_avg = stat_totals

        fig = go.Bar(x=stats, y=stat_avg)
        title_text = f"Average stat values (n={len(data['box_pokemon'])})"
        graph_div_avg_stat = plotly.offline.plot({"data": [fig], 
                                         "layout_title_text": title_text,
                                         }, auto_open=False, output_type="div",
                                         
                                         ) 
        data['graph_div_avg_stat'] = graph_div_avg_stat


        # Create pie chart for types

        # The counter data type is basically a dictionary that stores frequencies
        type_counter = Counter()

        for p in data['box_pokemon']:
            species = p.species
            
            type_counter[PokemonType(species.type1).name] += 1
            if species.type2:
                type_counter[PokemonType(species.type2).name] += 1

        # Separate labels and values
        labels = list(type_counter.keys())
        values = list(type_counter.values())

        fig = go.Pie(labels=labels, values=values)
        title_text = f"Type count (n={len(data['box_pokemon'])})"
        graph_div_type = plotly.offline.plot({"data": [fig], 
                                         "layout_title_text": title_text,
                                         }, auto_open=False, output_type="div",
                                         
                                         ) 
        data['graph_div_type'] = graph_div_type

        return data



class ShowCaughtPokemonView(DetailView):
    '''Display the an instance of a caught pokemon'''

    model = HasCaughtPokemon
    template_name = "project/show_caught_pokemon.html"
    context_object_name = "pokemon"



class CreateTrainerView(CreateView):
    '''A view to handle creation of a new Trainer.
    (1) display the HTML form to user (GET)
    (2) process the form submission and store the new Trainer object (POST)
    '''

    form_class = CreateTrainerForm
    template_name = "project/create_trainer_form.html"

class CreateMoveView(CreateView):
    '''A view to handle creation of a new Move.
    (1) display the HTML form to user (GET)
    (2) process the form submission and store the new Move object (POST)
    '''

    form_class = CreateMoveForm
    template_name = "project/create_move_form.html"

    def get_success_url(self):
        return reverse('show_all_moves')

class CreatePokemonSpeciesView(CreateView):
    '''A view to handle creation of a new Pokemon Species.
    (1) display the HTML form to user (GET)
    (2) process the form submission and store the new species object (POST)
    '''

    form_class = CreatePokemonSpeciesForm
    template_name = "project/create_species_form.html"


    def form_valid(self, form):
        ''' Form valid class used to check if pokemon doenst have duplicate type '''
        
        if 'type1' in self.request.POST and 'type2' in self.request.POST and (self.request.POST['type1'] == self.request.POST['type2']):  # Validate the user form
            form.add_error(None, "Type 1 and Type 2 must be different.")
            return self.form_invalid(form)
        else:
            return super().form_valid(form)
        

class CreateCaughtPokemonView(CreateView):
    '''A view to handle creation of a new Caught Pokemon Species.
    (1) display the HTML form to user (GET)
    (2) process the form submission and store the new object (POST)
    '''
    
    form_class = CreateCaughtPokemonForm
    template_name = "project/create_caught_form.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        pk = self.kwargs['pk']
        trainer = Trainer.objects.get(pk=pk)

        data['t'] = trainer
        return data

    def form_valid(self, form):
        ''' Form valid class used to check if pokemon doenst have duplicate type '''
        
        tpk = self.kwargs['pk']
        trainer = Trainer.objects.get(pk=tpk)

        spk = self.kwargs['pk1']
        species = Pokemon_Species.objects.get(pk=spk)

        form.instance.trainer = trainer
        form.instance.species = species

        if trainer.is_team_full() and ('in_team' in self.request.POST):  # Validate the user form
            form.add_error(None, "Team is already full.")
            return self.form_invalid(form)
        else:
            return super().form_valid(form)

        

class UpdateTrainerView(UpdateView):
    '''A view to handle update of a Trainer.
    (1) display the HTML form to user (GET)
    (2) process the form submission and update Trainer object (POST)
    '''
    model = Trainer
    form_class = UpdateTrainerForm
    template_name = "project/update_trainer_form.html"

class UpdatePokemonSpeciesView(UpdateView):
    '''A view to handle the update of a pokemon species.
    (1) display the HTML form to user (GET)
    (2) process the form submission and update the species object (POST)
    '''
    model = Pokemon_Species
    form_class = UpdatePokemonSpeciesForm
    template_name = "project/update_species_form.html"


class DeleteMoveView(DeleteView):
    ''' A view to delete a move from the database
        (1) display confirmation page to user (GET)
        (2) process the form submission and deletes move from the database (POST)
    '''

    model = Move
    template_name = "project/delete_move_form.html"
    context_object_name = 'move'

    def get_success_url(self):
        return reverse('show_all_moves')
    

class ToggleInTeamView(View):
    ''' Generic view to toggle wheather a caught pokemon is in it's trainers team or not, only receives post requests '''

    def post(self, request, *args, **kwargs):
        pk = self.kwargs["pk"]
        caught = HasCaughtPokemon.objects.get(pk=pk)

        caught.in_team = not caught.in_team
        caught.save()
        return redirect('show_trainer', caught.trainer.pk)
    


def search(dictionary, results):
        '''Method filters the query set contained in results based on the fields contained in the dictionary variable which is passed in as self.request.GET'''
        
        if 'nickname' in dictionary:
            nickname = dictionary['nickname']
            if nickname:
                # Get primary key of results that have the searched nickname within the actual nickname of the pokemon
                pks = [r.pk for r in results if nickname.lower() in r.nickname.lower()]
                
                
                results = HasCaughtPokemon.objects.filter(pk__in=pks)
                
        if 'stat' in dictionary:
            stat_to_search = dictionary['stat']
            if stat_to_search:
                # List comprehension to filter out caught pokemon that don't have their highest stat equal to stat_to_search, keep their primary key
               
                pks = [r.pk for r in results if r.get_highest_stat() == stat_to_search]
                
                
                # get back query set
                results = HasCaughtPokemon.objects.filter(pk__in=pks)
                
        if 'type' in dictionary:
            type = dictionary['type']
            type = int(type)  # Convert to integer
            
           
           # Here I did type > -1 because the normal type is represented as 0, and that was evaluating to false
            if type > -1:
                # Get all pokemon species with this type either in type 1 or type 2
                type1 = Pokemon_Species.objects.filter(type1=type)
                type2 = Pokemon_Species.objects.filter(type2=type)
                
                #  combine the query set
                species_with_type = type1 | type2 
                
                # filter based on this set
                results = results.filter(species__in=species_with_type)
        
        if 'min_level' in dictionary:
            min_level = dictionary['min_level']
            min_level = int(min_level)  # Convert to integer
            
            if min_level:
                results = results.filter(level__gte=min_level)

        if "max_level" in dictionary:
            max_level = dictionary['max_level']
            max_level = int(max_level)  # Convert to integer
            
            if max_level:
                results = results.filter(level__lte=max_level)

        
    
        return results
    

  
