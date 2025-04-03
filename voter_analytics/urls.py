# File: urls.py
# Author: João Pedro Rocha (jprocha@bu.edu), 04/01/2025
# Description: urls file for voter_analytics app, recieves http requests and routes them to correct function within views.py. Also handles routing for voters based on pk

from django.urls import path
from . import views 

urlpatterns = [
    # map the URL (empty string) to the view
	path(r'', views.VoterListView.as_view(), name='voters'),
    path(r'voter/<int:pk>', views.VoterDetailView.as_view(), name='voter'),
    path(r'graphs', views.VoterGraphView.as_view(), name='graphs'),
    # path(r'result/<int:pk>', views.ResultDetailView.as_view(), name='result_detail'),
    
]