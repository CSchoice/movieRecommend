from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse

def movie_board_list(request):
    pass

def create_movie_board_article(request):
    pass

def movie_board_article_detail(request, article_pk):
    pass

def edit_movie_board_article(request, article_pk):
    pass

def delete_movie_board_article(request, article_pk):
    pass

def create_comment(request, article_pk):
    pass

def edit_comment(request, article_pk, comment_pk):
    pass

def delete_comment(request, article_pk, comment_pk):
    pass

def like_movie_board_article(request, article_pk):
    pass