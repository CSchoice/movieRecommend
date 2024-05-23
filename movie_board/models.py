from django.db import models
from django.conf import settings
from movies.models import Movie

class MovieBoardComment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    # article = models.ForeignKey(MovieBoardArticle, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    