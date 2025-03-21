from django.urls import path
from django.conf import settings
from . import views
from .views import * #ShowAllView, ArticleView, RandomArticleView 

urlpatterns = [ 
    path('', RandomArticleView.as_view(), name='random'),
    path('show_all', ShowAllView.as_view(), name='show_all'),
    path('article/create', CreateArticleView.as_view(), name='create_article'),
    path('article/<int:pk>', ArticleView.as_view(), name='article'),
    path('article/<int:pk>/update', UpdateArticleView.as_view(), name='update_article'),
    path('article/<int:pk>/create_comment', CreateCommentView.as_view(), name='create_comment'),
    path('delete_comment/<int:pk>', DeleteCommentView.as_view(), name='delete_comment'),
]