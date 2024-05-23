# API 명세서


1. [API 문서](#API_문서)
2. [DB 모델](#DB_모델)

## API_문서 

### 유저 API

|         URL       |Method|설명 |
| ----------------- |------| ---------------------- |
| /accounts/signup/   |POST| 유저 회원가입  |
| /accounts/login/   |POST| 유저 로그인  |
| /accounts/logout/   |POST| 유저 로그아웃  |
| /accounts/<str:tar_username>/follow/   |POST| 유저 팔로우  |
| /accounts/check_login/   |POST| 유저 로그인여부 확인  |
| /accounts/<str:tar_username>/profile/   |GET| 회원 프로필 페이지  |
| /accounts/<str:tar_username>/followings/   |GET| 대상이 팔로잉 중인 유저 조회  |
| /accounts/<str:tar_username>/followers/   |GET| 대상을 팔로우 중인 유저 조회  |

### 자유게시판 API

|         URL       |Method  |            설명         |
| ----------------- | ------ | ---------------------- |
| /free_board/   |GET| 전체 게시물 조회  |
| /free_board/create/   |POST| 자유 게시판 게시글 작성  |
| /free_board/<int:article_pk>/   |GET| 자유 게시판 게시글 상세 정보  |
| /free_board/<int:article_pk>/edit/   |PUT| 자유 게시판 게시글 수정  |
| /free_board/<int:article_pk>/edit/   |delete| 자유 게시판 게시글 삭제  |
| /free_board/<int:article_pk>/comment/   |POST| 자유 게시판 댓글 작성  |
| /free_board/<int:article_pk>/comment/{comment_pk}/   |PUT| 자유 게시판 댓글 수정  |
| /free_board/<int:article_pk>/comment/{comment_pk}/   |delete| 자유 게시판 댓글 삭제  |
| /free_board/<int:article_pk>/like/   |POST| 자유 게시판 게시글 좋아요  |

### 영화 리뷰 게시판 API

|         URL       |Method  |            설명         |
| ----------------- | ------ | ---------------------- |
| /movie_board/<int:movie_pk>/   |GET| 영화 댓글 조회  |
| /movie_board/<int:movie_id>/comment/   |POST| 영화 게시판 댓글 작성  |
| /movie_board/<int:movie_id>/comment/<int:comment_pk>/   |PUT| 영화 게시판 댓글 수정  |
| /movie_board/<int:movie_id>/comment/<int:comment_pk>/   |delete| 영화 게시판 댓글 삭제  |

### 영화 API

| URL | Method | 설명 |
| --- | ------ | --- |
| movies/list/ | GET | 영화 리스트 조회 |
| movies/detail/<int:db_movie_id>/ | GET | 영화 상세 정보 조회 |
| movies/filter-genre/<str:genre_name>/ | GET | 장르별 영화 필터링 |
| movies/filter-actor/<int:db_actor_id>/ | GET | 배우별 영화 필터링 |
| movies/emotion_recommend/ | GET | 감정 기반 영화 추천 |
| movies/personal_recommend/ | GET | 개인 맞춤 영화 추천 |
| movies/personal_recommend/save/ | POST | 선택한 영화 저장 |
| movies/like-movie/<int:db_movie_id>/ | POST | 영화 좋아요 |
| movies/save_new_movie_data/<int:db_movie_id>/ | POST | 새로운 영화 데이터 저장 |
| movies/movie_exist/<int:db_movie_id>/ | GET | 영화 존재 여부 확인 |
| movies/search_poster/ | POST | 영화 포스터 검색 |


## DB 모델

### User 모델

| Name       | Type           | Description             | DB Relationship       |
|------------|----------------|-------------------------|-----------------------|
| username   | CharField(150) | 사용자 이름             |                       |
| email      | EmailField     | 이메일                  |                       |
| nickname   | CharField(20)  | 닉네임                  |                       |
| role       | CharField(10)  | 역할                    |                       |
| followings | ManyToMany     | 팔로잉                  | 사용자:사용자 = M:N   |
| followers  | ManyToMany     | 팔로워                  | 사용자:사용자 = M:N   |

### MovieBoardComment 모델

| Name       | Type           | Description             | DB Relationship       |
|------------|----------------|-------------------------|-----------------------|
| article    | ForeignKey     | 관련 기사               | 기사:댓글 = 1:N       |
| user       | ForeignKey     | 작성자                  | 사용자:댓글 = 1:N     |
| content    | TextField      | 댓글 내용               |                       |
| created_at | DateTime       | 댓글 생성 날짜          |                       |
| updated_at | DateTime       | 댓글 수정 날짜          |                       |

### FreeBoardArticle 모델

| Name       | Type           | Description             | DB Relationship       |
|------------|----------------|-------------------------|-----------------------|
| title      | CharField(50)  | 게시물 제목             |                       |
| content    | CharField(500) | 게시물 내용             |                       |
| created_at | DateTime       | 게시물 생성 날짜        |                       |
| updated_at | DateTime       | 게시물 수정 날짜        |                       |
| user       | ForeignKey     | 작성자                  | 사용자:게시물 = 1:N   |
| like_user  | ManyToMany     | 좋아요 표시한 사용자    | 사용자:게시물 = M:N   |

### FreeBoardComment 모델

| Name       | Type           | Description             | DB Relationship       |
|------------|----------------|-------------------------|-----------------------|
| article    | ForeignKey     | 관련 게시물             | 게시물:댓글 = 1:N     |
| user       | ForeignKey     | 작성자                  | 사용자:댓글 = 1:N     |
| content    | TextField      | 댓글 내용               |                       |
| created_at | DateTime       | 댓글 생성 날짜          |                       |
| updated_at | DateTime       | 댓글 수정 날짜          |                       |

### Genre 모델

| Name | Type          | Description | DB Relationship |
|------|---------------|--------------|-----------------|
| name | CharField(20) | 장르 이름    |                 |

### Actor 모델

| Name | Type          | Description | DB Relationship |
|------|---------------|--------------|-----------------|
| name | CharField(20) | 배우 이름    |                 |
|  db_actor_id | CharField(20) | 배우 id    |                 |
| profile_path | CharField(200) | 포스터 경로             |                       |
| character | CharField(20) | 역할    |                 |
| popularity | FloatField | 인기도    |                 |

### Director 모델

| Name | Type          | Description | DB Relationship |
|------|---------------|--------------|-----------------|
| name | CharField(20) | 감독 이름    |                 |
|  db_director_id | CharField(20) | 감독 id    |                 |
| profile_path | CharField(200) | 포스터 경로             |                       |
| job | CharField(20) | 직업    |                 |
| popularity | FloatField | 인기도    |                 |

### Movie 모델

| Name         | Type           | Description             | DB Relationship       |
|--------------|----------------|-------------------------|-----------------------|
| title        | CharField(50)  | 영화 제목               |                       |
| overview     | CharField(400) | 영화 개요               |                       |
| release_date | DateField      | 개봉일                  |                       |
| popularity   | FloatField     | 인기도                  |                       |
| vote_average | FloatField     | 평균 평점               |                       |
| poster_path  | CharField(200) | 포스터 경로             |                       |
| runtime      | IntegerField   | 상영 시간               |                       |
| genres       | ManyToMany     | 장르                    | 영화:장르 = M:N       |
| actors       | ManyToMany     | 배우                    | 영화:배우 = M:N       |
| directors       | ManyToMany     | 감독                    | 영화:감독 = M:N       |
| liked_user   | ForeignKey     | 좋아요 표시한 사용자    | 사용자:영화 = 1:N     |