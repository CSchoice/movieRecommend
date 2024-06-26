from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework import status
import json
from datetime import datetime
from .serializers import MovieListSerializer
import random
from .models import Movie, Actor, Genre, Director
import requests
from decouple import config

@api_view(['GET'])
def movie_list(request):
    movies = Movie.objects.filter(vote_average__gt=7)
    ran_size = min(10, movies.count())
    movies = random.sample(list(movies), ran_size)
    serializer = MovieListSerializer(movies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def save_new_movie_data(request, db_movie_id):
    url = f"https://api.themoviedb.org/3/movie/{db_movie_id}?language=ko-KR"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {config('TMDB_KEY')}"
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        item = response.json()
        
        # 각 영화에 대한 데이터 추출
        title = item.get('title')
        overview = item.get('overview')
        release_date_str = item.get('release_date')
        if release_date_str:  # release_date가 비어 있지 않은 경우
            try:
                release_date = datetime.strptime(release_date_str, '%Y-%m-%d').date()
            except ValueError:
                print(f"Invalid date format for movie: {title}. Skipping...")
                return Response({'message': f"Invalid date format for movie: {title}. Skipping..."}, status=400)
        else:
            release_date = None
        popularity = item.get('popularity')
        vote_average = item.get('vote_average')
        poster_path = item.get('poster_path')
        movie_id = item.get('id')
        genres = item.get('genres')
        
        # 장르 데이터 추출
        genre_ids = [genre['id'] for genre in genres] if genres else []
        
        # 영화 데이터 저장
        movie, created = Movie.objects.get_or_create(
            db_movie_id=movie_id,
            defaults={
                'title': title,
                'overview': overview,
                'release_date': release_date,
                'popularity': popularity,
                'vote_average': vote_average,
                'poster_path': poster_path,
            }
        )
        
        # 장르 데이터 저장
        if created:  # 새로운 영화인 경우에만
            for genre_id in genre_ids:
                genre, _ = Genre.objects.get_or_create(db_genre_id=genre_id)  # 이 부분을 수정합니다.
                movie.genres.add(genre)
        
    # 배우 정보 저장
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?language=ko-KR"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5NzBmZjQxMDZkN2M3NWQ4YThiMDYwNzhlMzUxMjgwZiIsInN1YiI6IjY2Mjc0MzliYWY5NTkwMDE2NDY5MzQ5MiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.JAyRCq0NoCjWHtBG6mp5xtIMvf5gpqgJTg_7S-SGTa0"
    }

    response = requests.get(url, headers=headers)
    from pprint import pprint
    if response.status_code == 200:
        item = response.json()
        # movie_id = item["id"]
        cast_list = item["cast"]

        # 영화 정보 생성
        movie = Movie.objects.get(
            db_movie_id=movie_id,
            # 다른 필드들을 설정하십시오.
        )
        pprint(cast_list)
        # 배우 정보 생성 및 연결
        for cast_data in cast_list[0:5]:
            actor_id = cast_data["id"]
            actor, _ = Actor.objects.get_or_create(
                db_actor_id=actor_id,
                defaults={
                "name": cast_data["name"],
                "profile_path": cast_data["profile_path"],
                "character": cast_data["character"],
                "popularity": cast_data["popularity"],
                }
            )

            movie.actors.add(actor)
            
        #감독 데이터 추가
        # movie_id = item["id"]
        cast_list = item["crew"]
        filtered_crew = [member for member in cast_list if member['job'] == 'Director'][0]

        # 영화 정보 생성
        movie = Movie.objects.get(
            db_movie_id=movie_id,
            # 다른 필드들을 설정하십시오.
        )
        # 배우 정보 생성 및 연결
        director_id = filtered_crew["id"]
        director, _ = Director.objects.get_or_create(
            db_director_id=director_id,
            defaults={
            "name": filtered_crew["name"],
            "profile_path": filtered_crew["profile_path"],
            "job": filtered_crew["job"],
            "popularity": filtered_crew["popularity"],
            }
        )

        movie.directors.add(director)
        
        return Response({'message': 'Movie data saved successfully.'}, status=200)
    else:
        return Response({'message': 'Failed to fetch movie data from API.'}, status=500)

@api_view(['GET'])
def movie_filter_by_genre(request, genre_name):
    genre = get_object_or_404(Genre, name=genre_name)
    movies = Movie.objects.filter(genres=genre)
    ran_size = min(10, movies.count())
    movies = random.sample(list(movies), ran_size)
    serializer = MovieListSerializer(movies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def movie_filter_by_actor(request, db_actor_id):
    actor = get_object_or_404(Actor, db_actor_id=db_actor_id)
    movies = Movie.objects.filter(actors=actor)
    ran_size = min(10, movies.count())
    movies = random.sample(list(movies), ran_size)
    serializer = MovieListSerializer(movies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

def emotion_based_movie_list(request):
    pass

def personal_based_movie_list(request):
    pass

def save_selected_movie(request):
    pass

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def like_movie(request, db_movie_id):
    movie = get_object_or_404(Movie, db_movie_id=db_movie_id)
    if movie.like_user.filter(pk=request.user.pk).exists():
        # 이미 좋아요를 한 경우, 좋아요 취소
        movie.like_user.remove(request.user)
        return Response({"message": "영화 좋아요 취소"}, status=status.HTTP_200_OK)
    else:
        # 좋아요 추가
        movie.like_user.add(request.user)
        return Response({"message": "영화 좋아요 성공"}, status=status.HTTP_200_OK)
    
@api_view(['GET'])
def movie_detail(request, db_movie_id):
    movie = get_object_or_404(Movie, db_movie_id=db_movie_id)
    serializer = MovieListSerializer(movie)
    return Response(serializer.data)

@api_view(['GET'])
def movie_exist(request, db_movie_id):
    try:
        movie = Movie.objects.get(db_movie_id=db_movie_id)
        serializer = MovieListSerializer(movie)
        return Response({"message": "영화가 db에 있습니다", "movie": serializer.data}, status=status.HTTP_200_OK)
    except:
            url = f"https://api.themoviedb.org/3/movie/{db_movie_id}?language=ko-KR"

            headers = {
                "accept": "application/json",
                "Authorization": f"Bearer {config('TMDB_KEY')}"
            }

            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                item = response.json()
                
                # 각 영화에 대한 데이터 추출
                title = item.get('title')
                overview = item.get('overview')
                release_date_str = item.get('release_date')
                if release_date_str:  # release_date가 비어 있지 않은 경우
                    try:
                        release_date = datetime.strptime(release_date_str, '%Y-%m-%d').date()
                    except ValueError:
                        print(f"Invalid date format for movie: {title}. Skipping...")
                        return Response({'message': f"Invalid date format for movie: {title}. Skipping..."}, status=400)
                else:
                    release_date = None
                popularity = item.get('popularity')
                vote_average = item.get('vote_average')
                poster_path = item.get('poster_path')
                movie_id = item.get('id')
                genres = item.get('genres')
                
                # 장르 데이터 추출
                genre_ids = [genre['id'] for genre in genres] if genres else []
                
                # 영화 데이터 저장
                movie, created = Movie.objects.get_or_create(
                    db_movie_id=movie_id,
                    defaults={
                        'title': title,
                        'overview': overview,
                        'release_date': release_date,
                        'popularity': popularity,
                        'vote_average': vote_average,
                        'poster_path': poster_path,
                    }
                )
                
                # 장르 데이터 저장
                if created:  # 새로운 영화인 경우에만
                    for genre_id in genre_ids:
                        genre, _ = Genre.objects.get_or_create(db_genre_id=genre_id)  # 이 부분을 수정합니다.
                        movie.genres.add(genre)
                
            # 배우 정보 저장
            url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?language=ko-KR"

            headers = {
                "accept": "application/json",
                "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5NzBmZjQxMDZkN2M3NWQ4YThiMDYwNzhlMzUxMjgwZiIsInN1YiI6IjY2Mjc0MzliYWY5NTkwMDE2NDY5MzQ5MiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.JAyRCq0NoCjWHtBG6mp5xtIMvf5gpqgJTg_7S-SGTa0"
            }

            response = requests.get(url, headers=headers)
            from pprint import pprint
            if response.status_code == 200:
                item = response.json()
                # movie_id = item["id"]
                cast_list = item["cast"]

                # 영화 정보 생성
                movie = Movie.objects.get(
                    db_movie_id=movie_id,
                    # 다른 필드들을 설정하십시오.
                )
                pprint(cast_list)
                # 배우 정보 생성 및 연결
                for cast_data in cast_list[0:5]:
                    actor_id = cast_data["id"]
                    actor, _ = Actor.objects.get_or_create(
                        db_actor_id=actor_id,
                        defaults={
                        "name": cast_data["name"],
                        "profile_path": cast_data["profile_path"],
                        "character": cast_data["character"],
                        "popularity": cast_data["popularity"],
                        }
                    )

                    movie.actors.add(actor)
                    
                #감독 데이터 추가
                # movie_id = item["id"]
                cast_list = item["crew"]
                filtered_crew = [member for member in cast_list if member['job'] == 'Director'][0]

                # 영화 정보 생성
                movie = Movie.objects.get(
                    db_movie_id=movie_id,
                    # 다른 필드들을 설정하십시오.
                )
                # 배우 정보 생성 및 연결
                director_id = filtered_crew["id"]
                director, _ = Director.objects.get_or_create(
                    db_director_id=director_id,
                    defaults={
                    "name": filtered_crew["name"],
                    "profile_path": filtered_crew["profile_path"],
                    "job": filtered_crew["job"],
                    "popularity": filtered_crew["popularity"],
                    }
                )

                movie.directors.add(director)
                movie = Movie.objects.get(db_movie_id=db_movie_id)
                serializer = MovieListSerializer(movie)
                return Response({'message': 'Movie data saved successfully.', "movie": serializer.data}, status=200)
            else:
                return Response({'message': 'Failed to fetch movie data from API.', "movie": serializer.errors}, status=500)

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

        # 각 장르에 대해 Genre 모델에 레코드 생성 및 연결
        for genre_id in genres:
            genre, created = Genre.objects.get_or_create(db_genre_id=genre_id)
            movie.genres.add(genre)
    return Response({'message': 'Movie data saved successfully'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def search_poster(request):
    movie_list = request.data['movies']
    new_movie_list = []
    for movie_name in movie_list:
        url = f"https://api.themoviedb.org/3/search/movie?query={movie_name}&include_adult=false&language=ko-KR&page=1"

        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5NzBmZjQxMDZkN2M3NWQ4YThiMDYwNzhlMzUxMjgwZiIsInN1YiI6IjY2Mjc0MzliYWY5NTkwMDE2NDY5MzQ5MiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.JAyRCq0NoCjWHtBG6mp5xtIMvf5gpqgJTg_7S-SGTa0"
        }

        response = requests.get(url, headers=headers)
        try: 
            if response.status_code == 200:
                item = response.json()
                movie = item['results'][0]
                db_movie_id = movie['id']
                poster_path = movie['poster_path']
                title = movie['title']
                
                result = {'db_movie_id':db_movie_id, 'poster_path':f'https://image.tmdb.org/t/p/original/{poster_path}', 'title':title}
                new_movie_list.append(result)
        except: continue

    return Response(new_movie_list)

@api_view(['POST'])
def get_movie_id(request):
    movies = Movie.objects.all()
    movie_id_lst = [movie.db_movie_id for movie in movies]
    return Response({'movies': movie_id_lst})

# @api_view(['GET'])
# def save_director_data(request):
#     with open('movies/data/directors.json', 'r', encoding='utf-8') as f:
#         data = json.load(f)

#     for item in data:
#         movie_id = item["id"]
#         cast_list = item["cast"]

#         # 영화 정보 생성
#         movie = Movie.objects.get(
#             db_movie_id=movie_id,
#             # 다른 필드들을 설정하십시오.
#         )

#         # 배우 정보 생성 및 연결
#         for cast_data in cast_list:
#             actor_id = cast_data["id"]
#             actor, _ = Actor.objects.get_or_create(
#                 db_actor_id=actor_id,
#                 defaults={
#                 "name": cast_data["name"],
#                 "profile_path": cast_data["profile_path"],
#                 "character": cast_data["character"],
#                 }
#             )
#             movie.actors.add(actor)

#         # 장르 정보 생성 및 연결
#         # 필요하다면 비슷한 방식으로 장르 정보를 처리할 수 있습니다.

#         # 영화 정보 저장
#         movie.save()
#     return Response({'message': 'Movie data saved successfully'}, status=status.HTTP_201_CREATED)

def save_director_data(request):
    # directors.json 파일 읽기
    with open('movies/data/directors.json', 'r', encoding='utf-8') as f:
        directors_data = json.load(f)

    # 데이터베이스에 저장
    for movie_id, directors_list in directors_data.items():
        try:
            # 영화 정보 가져오기
            movie = Movie.objects.get(db_movie_id=movie_id)
        except Movie.DoesNotExist:
            # 해당하는 영화 정보가 없으면 건너뛰기
            continue

        # 감독 정보를 영화에 저장
        for director_info in directors_list:
            # 감독 정보 추출
            director_id = director_info['id']
            name = director_info['name']
            profile_path = director_info['profile_path']
            job = director_info.get('job', None)  # 'job' 키가 없을 경우 None으로 설정
            popularity = director_info.get('popularity', None)  # 'popularity' 키가 없을 경우 None으로 설정

            # Director 모델에 저장
            director, created = Director.objects.get_or_create(
                db_director_id=director_id,
                defaults={'name': name, 'profile_path': profile_path, 'job': job, 'popularity': popularity}
            )

            # 영화에 감독 정보 추가
            movie.directors.add(director)

    return Response({'message': 'Director data saved successfully'})