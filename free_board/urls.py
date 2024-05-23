"""
URL configuration for movieRecommendpjt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.free_board_list, name='free_board_list'),
    path('article/', views.create_free_board_article, name='create_free_board_article'),
    path('<int:article_pk>/', views.free_board_article_detail, name='free_board_article_detail'),
    path('<int:article_pk>/edit/', views.edit_free_board_article, name='edit_free_board_article'),
    path('<int:article_pk>/comment/', views.create_free_board_comment, name='create_free_board_comment'),
    path('<int:article_pk>/comment/<int:comment_pk>/', views.edit_free_board_comment, name='edit_free_board_comment'),
    path('<int:article_pk>/like/', views.like_free_board_article, name='like_free_board_article'),
]