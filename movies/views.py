from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework import status
import json
from datetime import datetime
from .models import Movie, Genre
from .serializers import MovieSerializer

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
            Genre.objects.update_or_create(genre_id=item['pk'], defaults={'name': item['name']})

        return Response({'message': 'Data saved successfully'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


from .models import Movie, Genre

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
            release_date = None  # release_date가 비어 있으면 None을 할당
        popularity = item.get('popularity')
        vote_average = item.get('vote_average')
        poster_path = item.get('poster_path')
        movie_id = item.get('id')
        genres = item.get('genre_ids')

        # 영화 데이터 저장
        movie = Movie.objects.create(
            title=title,
            overview=overview,
            release_date=release_date,
            popularity=popularity,
            vote_average=vote_average,
            poster_path=poster_path,
            movie_id=movie_id,
        )

        # 각 장르에 대해 Genre 모델에 레코드 생성 및 연결
        for genre_id in genres:
            genre, created = Genre.objects.get_or_create(genre_id=genre_id)
            movie.genres.add(genre)




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