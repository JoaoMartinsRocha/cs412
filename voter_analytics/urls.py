from django.urls import path
from . import views 

urlpatterns = [
    # map the URL (empty string) to the view
	path(r'', views.VoterListView.as_view(), name='voters'),
    path(r'voter/<int:pk>', views.VoterDetailView.as_view(), name='voter'),
    path(r'graphs', views.VoterGraphView.as_view(), name='graphs'),
    # path(r'result/<int:pk>', views.ResultDetailView.as_view(), name='result_detail'),
    
]