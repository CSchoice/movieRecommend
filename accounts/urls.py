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
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path('login/', views.custom_login_view, name='custom_login'),
    path('<str:tar_username>/follow/', views.follow_user, name='user_follow'),
    path('<str:tar_user_pk>/profile/', views.user_profile, name='user_profile'),
    path('<str:tar_username>/followings/', views.user_followings, name='user_followings'),
    path('<str:tar_username>/followers/', views.user_followers, name='user_followers'),
    path('api-token-auth/', obtain_auth_token),
    path('', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),
    path('csrf/', views.get_csrf_token, name='get_csrf_token'),
]