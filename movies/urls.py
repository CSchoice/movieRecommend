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
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.movie_list, name='movie_list'),
    path('filter-genre/', views.movie_filter_by_genre, name='movie_filter_by_genre'),
    path('filter-actor/', views.movie_filter_by_actor, name='movie_filter_by_actor'),
    path('emotion_recommend/', views.emotion_based_movie_list, name='emotion_based_movie_list'),
    path('personal_recommend/', views.personal_based_movie_list, name='personal_based_movie_list'),
    path('personal_recommend/save/', views.save_selected_movie, name='save_selected_movie'),
    # path('<int:movie_id>/like_movie/', views.like_movie, name='like_movie'),
    path('save_movie_data/',views.save_movie_data, name='save_movie_data'),
]
