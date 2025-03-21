from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from.models import Article, Comment
from .forms import CreateArticleForm, CreateCommentForm, UpdateArticleForm
import random
from django.urls import reverse
# Create your views here.

class ShowAllView(ListView):

    model = Article
    template_name = "blog/show_all.html"
    context_object_name = "articles"

class ArticleView(DetailView):
    '''Display a singe Article'''

    model = Article
    template_name = "blog/article.html"
    context_object_name = "article"


class RandomArticleView(DetailView):
    '''Display a singe Article'''

    model = Article
    template_name = "blog/article.html"
    context_object_name = "article"

    # methods
    def get_object(self):
        all_articles = Article.objects.all()
        article = random.choice(all_articles)
        return article
    

class CreateArticleView(CreateView):
    '''A view to handle creation of a new Article.
    (1) display the HTML form to user (GET)
    (2) process the form submission and store the new Article object (POST)
    '''

    form_class = CreateArticleForm
    template_name = "blog/create_article_form.html"

class CreateCommentView(CreateView):
    '''A view to create a new comment on an Article and save it to the database.'''

    form_class = CreateCommentForm
    template_name = "blog/create_comment_form.html"
    
    def get_success_url(self):
        '''Return the URL to redirect to after successfully submitting form.'''
        # return reverse('show_all')
        ## note: this is not ideal, because we are redirected to the main page.
        pk = self.kwargs['pk']
        return reverse('article', kwargs={'pk':pk})
    
    def get_context_data(self):
        '''Return the dictionary of context variables for use in the template.'''

        # calling the superclass method
        context = super().get_context_data()

        # find/add the article to the context data
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        article = Article.objects.get(pk=pk)

        # add this article into the context dictionary:
        context['article'] = article
        return context

    def form_valid(self, form):
        '''This method handles the form submission and saves the 
        new object to the Django database.
        We need to add the foreign key (of the Article) to the Comment
        object before saving it to the database.
        '''
        
		# instrument our code to display form fields: 
        print(f"CreateCommentView.form_valid: form.cleaned_data={form.cleaned_data}")
        
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        article = Article.objects.get(pk=pk)
        # attach this article to the comment
        form.instance.article = article # set the FK

        # delegate the work to the superclass method form_valid:
        return super().form_valid(form)

class UpdateArticleView(UpdateView):

    model = Article
    form_class = UpdateArticleForm
    template_name = "blog/update_article_form.html"


class DeleteCommentView(DeleteView):
    '''A view to delete a comment and remove it from the database.'''

    template_name = "blog/delete_comment_form.html"
    model = Comment
    context_object_name = 'comment'

    def get_success_url(self):
        '''Return the URL to redirect to after successfully submitting form.'''
        
        ## Find pk of comment first
        pk = self.kwargs['pk']
        # Find  the comment object
        comment = Comment.objects.get(pk=pk)

        article = comment.article

        return reverse('article', kwargs={'pk': article.pk})
        