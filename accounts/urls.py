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
    path('accounts/signup/', views.user_signup, name='user_signup'),
    path('accounts/login/', views.user_login, name='user_login'),
    path('accounts/logout/', views.user_logout, name='user_logout'),
    path('accounts/<int:user_pk>/control/', views.user_control_page, name='user_control_page'),
    path('accounts/<int:user_pk>/control/', views.modify_user_info, name='modify_user_info'),
    path('accounts/<int:tar_user_pk>/follow/', views.follow_user, name='follow_user'),
    path('accounts/check_login/', views.check_login_status, name='check_login_status'),
    path('accounts/<str:tar_username>/profile/', views.user_profile_page, name='user_profile_page'),
    path('accounts/<str:tar_username>/followings/', views.view_followings, name='view_followings'),
    path('accounts/<str:tar_username>/followers/', views.view_followers, name='view_followers'),
]