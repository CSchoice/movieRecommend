from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json
from datetime import datetime
from .models import Movie
from .serializers import MovieSerializer

def save_movie_data(data):
    with open('movies/data/movie_data.json', 'r', encoding='utf-8') as f:
        movie_data = json.load(f)
    
    for item in movie_data:
        title = item.get('title')
        overview = item.get('overview')
        print(item.get('release_date'))
        release_date_str = item.get('release_date')
        if release_date_str:  # release_date가 비어 있지 않은 경우
            try:
                release_date = datetime.strptime(release_date_str, '%Y-%m-%d').date()
            except ValueError:
                print(f"Invalid date format for movie: {title}. Skipping...")
                continue
        else:
            release_date = None  # release_date가 비어 있으면 None을 할당
        popularity = item.get('popularity')
        vote_average = item.get('vote_average')
        poster_path = item.get('poster_path')
        movie_id = item.get('id')
        genres = item.get('genre_ids')

        # 장르를 PrimaryKeyRelatedField로 전달하여 시리얼라이저에 맞게 준비
        genres_ids = []
        for genre_id in genres:
            genres_ids.append(genre_id)

        # 영화 데이터 시리얼라이즈
        serializer = MovieSerializer(data={
            'title': title,
            'overview': overview,
            'release_date': release_date,
            'popularity': popularity,
            'vote_average': vote_average,
            'poster_path': poster_path,
            'movie_id': movie_id,
            'genres': genres_ids  # 시리얼라이저에 맞게 장르 id 리스트 전달
        })

        # 시리얼라이즈가 유효한지 확인하고 저장
        if serializer.is_valid():
            serializer.save()
        #     return Response({'message':'영화 저장 성공'}, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def movie_list(request):
    pass

def movie_filter_by_genre(request):
    pass

def movie_filter_by_actor(request):
    pass

def emotion_based_movie_list(request):
    pass

def personal_based_movie_list(request):
    pass

def save_selected_movie(request):
    pass

# def like_movie(request, movie_id):
#     try:
#         movie = get_object_or_404(Movie, movie_id=movie_id)
#         if movie.like_user.filter(pk=request.user.pk).exists():
#             # 이미 좋아요를 한 경우, 좋아요 취소
#             movie.like_user.remove(request.user)
#             return Response({"message": "게시글 좋아요 취소"}, status=status.HTTP_200_OK)
#         else:
#             # 좋아요 추가
#             movie.like_user.add(request.user)
#             return Response({"message": "게시글 좋아요 성공"}, status=status.HTTP_200_OK)
#     except:
#         serializer = MovieSerializer(data=request.data)