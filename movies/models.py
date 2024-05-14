from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=20)


class Movie(models.Model):
    title = models.CharField(max_length=50)
    title = models.CharField(max_length=400)
    release_date = models.DateField()
    popularity = models.FloatField()
    vote_average = models.FloatField()
    poster_path = models.CharField(max_length=200)
    runtiem = models.IntegerField()
    genres = models.ManyToManyField(Genre)
    