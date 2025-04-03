# File: views.py
# Author: João Pedro Rocha (jprocha@bu.edu), 04/01/2025
# Description: Views file for voter_analytics app, recieves http requests and responds with correct html template. 
# Vews include showing all voter instances, showing a single voter instance, and one displaying graphs describing voter intsances

from django.shortcuts import render

from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from . models import Voter
from datetime import date
from django.db.models import Min, Max

import plotly
import plotly.graph_objs as go



class VoterDetailView(DetailView):
    '''View to show detail page for one voter.'''

    template_name = 'voter_analytics/voter_detail.html'
    model = Voter
    context_object_name = 'v'

class VoterGraphView(ListView):
    '''Creates plorly graphs for the specified set of voters filtered by the search form'''
    template_name = 'voter_analytics/graphs.html'
    model = Voter
    context_object_name = 'voters'


    def get_context_data(self, **kwargs) :
        '''
        Provide context variables for use in template, in this case, the graphs in form of divs
        '''
        
        # start with superclass context
        context = super().get_context_data(**kwargs)
        voters = context['voters']

        voters = search(self.request.GET, voters) # filter based on search form

        # Grab min year or max year in search
        if 'min_dob_year' in self.request.GET:
            min_year = self.request.GET['min_dob_year']
        else:
            min_year = '1920' # default is 1920
        
        if 'max_dob_year' in self.request.GET:
            max_year = self.request.GET['max_dob_year']
        else:
            max_year = '2004'# feault is 2004

        
        lables = [] # all years present
        values = [] # number of voters with a  specific dob

        # for loop populates values
        for i in range(int(min_year), int(max_year) + 1):
            min_date_format = date(i, 1, 1)
            max_date_format = date(i + 1, 1, 1)
            lables += [i]
            query = voters.filter(dob__gte=min_date_format)
            query = query.filter(dob__lt=max_date_format)
            values += [len(query)] 


        # create histogram of distribution by birth year:
        
        fig = go.Bar(x=lables, y=values)
        title_text = f"Voter distribution by year of birth (n={len(voters)})"
        graph_div_age_dist = plotly.offline.plot({"data": [fig], 
                                         "layout_title_text": title_text,
                                         }, auto_open=False, output_type="div",
                                         
                                         ) 
        context['graph_div_age_dist'] = graph_div_age_dist

        # Make Pie chart

        lables = [] # all possible party affiliations
        values = [] # number of voters with in that party

        unique_values = voters.values('party_affiliation').distinct() # Get unique values in search results

        for item in unique_values: # loop through them and count the number of values using len()
            lables += [item['party_affiliation']]
            values += [len(voters.filter(party_affiliation=item['party_affiliation']))] # Access the value using the dictionary key

        # create figure
        fig = go.Pie(labels=lables, values=values)

        title_text = f"Voter distribution by party affiliation (n={len(voters)})"

        graph_div_party = plotly.offline.plot({"data": [fig], 
                                         "layout_title_text": title_text,
                                         }, auto_open=False, output_type="div"
                                         
        ) 

                        
        context['graph_div_party'] = graph_div_party

       
        # Make second histogram
        lables = ["v20state", "v21town", "v21primary", "v22general", "v23town"] # all elections
        # Just filter by if they voted in that election or not
        values = [
            len(voters.filter(v20state=True)),
            len(voters.filter(v21town=True)),
            len(voters.filter(v21primary=True)),
            len(voters.filter(v22general=True)),
            len(voters.filter(v23town=True))
        ] # number of voters with a  specific dob

        # create figure
        
        fig = go.Bar(x=lables, y=values)
        title_text = f"Vote count by election (n={len(voters)})"
        graph_div_age_election = plotly.offline.plot({"data": [fig], 
                                         "layout_title_text": title_text,
                                         }, auto_open=False, output_type="div",
                                         
                                         ) 
        context['graph_div_election'] = graph_div_age_election


        return context 



class VoterListView(ListView):
    '''View to display all voters '''

    template_name = 'voter_analytics/voters.html'
    model = Voter
    context_object_name = 'voters'
    paginate_by = 100

    def get_queryset(self):
        
        # start with entire queryset
        results = super().get_queryset().order_by('first_name', 'last_name')
        
        # return filtered search results
        return search(self.request.GET, results)
    
    def get_context_data(self, **kwargs):
        """Pass filtered query parameters to the template, this makes sure that when you switch pages on the template you still filter by the search."""
        context = super().get_context_data(**kwargs)
        
        # Create a mutable copy of request.GET
        params = self.request.GET.copy()
        
        # Remove 'page' if it exists
        params.pop('page', None)
        
        # Add the cleaned parameters to the context
        context['params'] = params
        
        return context


def search(dictionary, results):
        '''Method filters the query set contained in results based on the fields contained in the dictionary variable which is passed in as self.request.GET'''
        
        if 'party_affiliation' in dictionary:
            party = dictionary['party_affiliation']
            if party:
                results = results.filter(party_affiliation=party)

        if 'voter_score' in dictionary:
            voter_score = dictionary['voter_score']
            if voter_score:
                results = results.filter(voter_score=voter_score)

        if 'min_dob_year' in dictionary:
            min_year = dictionary['min_dob_year']
            min_year = int(min_year)  # Convert to integer
            min_year = date(min_year, 1, 1)  # Create a full date object
            if min_year:
                results = results.filter(dob__gte=min_year)
        
        if 'max_dob_year' in dictionary:
            max_year = dictionary['max_dob_year']
            max_year = int(max_year)  # Convert to integer
            max_year = date(max_year, 12, 31)  # Create a full date object
            if max_year:
                results = results.filter(dob__lte=max_year)

        if "v20state" in dictionary:
            results = results.filter(v20state=True)

        if "v21town" in dictionary:
            results = results.filter(v21town=True)

        if "v21primary" in dictionary:
            results = results.filter(v21primary=True)

        if "v22general" in dictionary:
            results = results.filter(v22general=True)

        if "v23town" in dictionary:
            results = results.filter(v23town=True)
           
        return results