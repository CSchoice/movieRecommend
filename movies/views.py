from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework import status
import json
from datetime import datetime
from .models import Movie, Genre
from .serializers import MovieSerializer
import random

@api_view(['GET'])
def movie_list(request):
    movies = Movie.objects.filter(vote_average__gt=7)
    ran_size = min(10, movies.count())
    movies = random.sample(list(movies), ran_size)
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def save_genre_data(request):
    data = [
        {"pk": 28, "name": "액션"},
        {"pk": 12, "name": "모험"},
        {"pk": 16, "name": "애니메이션"},
        {"pk": 35, "name": "코미디"},
        {"pk": 80, "name": "범죄"},
        {"pk": 99, "name": "다큐멘터리"},
        {"pk": 18, "name": "드라마"},
        {"pk": 10751, "name": "가족"},
        {"pk": 14, "name": "판타지"},
        {"pk": 36, "name": "역사"},
        {"pk": 27, "name": "공포"},
        {"pk": 10402, "name": "음악"},
        {"pk": 9648, "name": "미스터리"},
        {"pk": 10749, "name": "로맨스"},
        {"pk": 878, "name": "SF"},
        {"pk": 10770, "name": "TV 영화"},
        {"pk": 53, "name": "스릴러"},
        {"pk": 10752, "name": "전쟁"},
        {"pk": 37, "name": "서부"}
    ]

    try:
        for item in data:
            Genre.objects.update_or_create(db_genre_id=item['pk'], defaults={'name': item['name']})
        return Response({'message': 'Movie data saved successfully'}, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
import json
from .models import Movie, Genre

@api_view(['GET'])
def save_movie_data(data):
    with open('movies/data/movie_data.json', 'r', encoding='utf-8') as f:
        movie_data = json.load(f)
    
    for item in movie_data:
        # 각 영화에 대한 데이터 추출
        title = item.get('title')
        overview = item.get('overview')
        release_date_str = item.get('release_date')
        if release_date_str:  # release_date가 비어 있지 않은 경우
            try:
                release_date = datetime.strptime(release_date_str, '%Y-%m-%d').date()
            except ValueError:
                print(f"Invalid date format for movie: {title}. Skipping...")
                continue
            
        else:
            release_date = None
        popularity = item.get('popularity')
        vote_average = item.get('vote_average')
        poster_path = item.get('poster_path')
        movie_id = item.get('id')
        if Movie.objects.filter(db_movie_id=movie_id).exists(): continue

        genres = item.get('genre_ids')
        # 영화 데이터 저장
        movie = Movie.objects.create(
            title=title,
            overview=overview,
            release_date=release_date,
            popularity=popularity,
            vote_average=vote_average,
            poster_path=poster_path,
            db_movie_id=movie_id,
        )

        # 각 장르에 대해 Genre 모델에 레코드 생성 및 연결
        for genre_id in genres:
            genre, created = Genre.objects.get_or_create(db_genre_id=genre_id)
            movie.genres.add(genre)
    return Response({'message': 'Movie data saved successfully'}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def movie_filter_by_genre(request, genre_name):
    genre = get_object_or_404(Genre, name=genre_name)
    movies = Movie.objects.filter(genres=genre)
    ran_size = min(10, movies.count())
    movies = random.sample(list(movies), ran_size)
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def movie_filter_by_actor(request, actor_name):
    # movies = Movie.objects.filter(actor=actor)
    ran_size = min(10, movies.count())
    movies = random.sample(list(movies), ran_size)
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

def emotion_based_movie_list(request):
    pass

def personal_based_movie_list(request):
    pass

def save_selected_movie(request):
    pass

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def like_movie(request, movie_id):
    movie = get_object_or_404(Movie, db_movie_id=movie_id)
    if movie.like_user.filter(pk=request.user.pk).exists():
        # 이미 좋아요를 한 경우, 좋아요 취소
        movie.like_user.remove(request.user)
        return Response({"message": "게시글 좋아요 취소"}, status=status.HTTP_200_OK)
    else:
        # 좋아요 추가
        movie.like_user.add(request.user)
        return Response({"message": "게시글 좋아요 성공"}, status=status.HTTP_200_OK)
    
    
import json
from datetime import datetime
from .models import Movie, Actor, Genre

@api_view(['GET'])
def save_actor_data(request):
    with open('movies/data/actor_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    for item in data:
        movie_id = item["id"]
        cast_list = item["cast"]

        # 영화 정보 생성
        movie = Movie.objects.get(
            db_movie_id=movie_id,
            # 다른 필드들을 설정하십시오.
        )

        # 배우 정보 생성 및 연결
        for cast_data in cast_list:
            actor_id = cast_data["id"]
            actor, _ = Actor.objects.get_or_create(
                db_actor_id=actor_id,
                defaults={
                "name": cast_data["name"],
                "profile_path": cast_data["profile_path"],
                "character": cast_data["character"],
                }
            )
            movie.actors.add(actor)

        # 장르 정보 생성 및 연결
        # 필요하다면 비슷한 방식으로 장르 정보를 처리할 수 있습니다.

        # 영화 정보 저장
        movie.save()