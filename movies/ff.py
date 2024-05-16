from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Movie, Genre
from .serializers import MovieSerializer
from datetime import datetime
import json

def save_movie_data(data):
    with open('movies/data/movie_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    for item in data:
        # 필요한 필드 추출
        title = item.get('title')
        overview = item.get('overview')
        release_date = datetime.strptime(item.get('release_date'), '%Y-%m-%d').date()
        popularity = item.get('popularity')
        vote_average = item.get('vote_average')
        poster_path = item.get('poster_path')
        movie_id = item.get('id')
        genres = item.get('genre_ids')

        # Movie 인스턴스 생성
        movie = Movie.objects.create(
            title=title,
            overview=overview,
            release_date=release_date,
            popularity=popularity,
            vote_average=vote_average,
            poster_path=poster_path,
            movie_id=movie_id
        )

        # 장르 추가
        for genre_id in genres:
            genre, _ = Genre.objects.get_or_create(id=genre_id)
            movie.genres.add(genre)

        # 저장
        movie.save()
save_movie_data()