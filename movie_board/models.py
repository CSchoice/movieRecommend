from django.db import models
from django.conf import settings
from movies.models import Movie, likedMovie

class MovieBoardArticle(models.Model):
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like_user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='movieboard_like_articles')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)


class MovieBoardComment(models.Model):
    article = models.ForeignKey(MovieBoardArticle, on_delete=models.CASCADE)
    userId = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)