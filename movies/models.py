from django.db import models
from django.conf import settings

class Genre(models.Model):
    name = models.CharField(max_length=20)
    db_genre_id = models.IntegerField(unique=True)

class Actor(models.Model):
    name = models.CharField(max_length=20)
    db_actor_id = models.IntegerField(unique=True)
    profile_path = models.CharField(max_length=200, blank=True, null=True)
    character = models.CharField(max_length=40, blank=True, null=True)
     
class Movie(models.Model):
    db_movie_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=50)
    overview = models.CharField(max_length=400)
    release_date = models.DateField(blank=True, null=True)
    popularity = models.FloatField(blank=True, null=True)
    vote_average = models.FloatField(blank=True, null=True)
    poster_path = models.CharField(max_length=200)
    like_user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_movies', null=True)
    actors = models.ManyToManyField(Actor, blank=True)
    genres = models.ManyToManyField(Genre)

# class likedMovie(models.Model):
#     title = models.CharField(max_length=50)
#     overview = models.CharField(max_length=400)
#     release_date = models.DateField()
#     popularity = models.FloatField()
#     vote_average = models.FloatField()
#     poster_path = models.CharField(max_length=200)
#     runtime = models.IntegerField()
#     genres = models.ManyToManyField(Genre)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
