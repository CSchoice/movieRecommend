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
| /accounts/{user_pk}/control   |GET| 회원정보 수정 페이지  |
| /accounts/{user_pk}/control   |POST| 회원정보 수정  |
| /accounts/{tar_user_pk}/follow/   |POST| 유저 팔로우  |
| /accounts/check_login/   |POST| 유저 로그인여부 확인  |
| /accounts/{tar_username}/profile/   |GET| 회원 프로필 페이지  |
| /accounts/{tar_username}/followings/   |GET| 대상이 팔로잉 중인 유저 조회  |
| /accounts/{tar_username}/followers/   |GET| 대상을 팔로우 중인 유저 조회  |

### 자유게시판 API

|         URL       |Method  |            설명         |
| ----------------- | ------ | ---------------------- |
| /free_board/   |GET| 전체 게시물 조회  |
| /free_board/create/   |POST| 자유 게시판 게시글 작성  |
| /free_board/{article_pk}/   |GET| 자유 게시판 게시글 상세 정보  |
| /free_board/{article_pk}/edit/   |PUT| 자유 게시판 게시글 수정  |
| /free_board/{article_pk}/edit/   |delete| 자유 게시판 게시글 삭제  |
| /free_board/{article_pk}/comment/   |POST| 자유 게시판 댓글 작성  |
| /free_board/{article_pk}/comment/{comment_pk}/   |PUT| 자유 게시판 댓글 수정  |
| /free_board/{article_pk}/comment/{comment_pk}/   |delete| 자유 게시판 댓글 삭제  |
| /free_board/{article_pk}/like/   |POST| 자유 게시판 게시글 좋아요  |

### 영화 리뷰 게시판 API

|         URL       |Method  |            설명         |
| ----------------- | ------ | ---------------------- |
| /movie_board/   |GET| 전체 게시물 조회  |
| /movie_board/create/{movie_pk}/   |POST| 영화 게시판 게시글 작성  |
| /movie_board/{article_pk}/   |GET| 영화 게시판 게시글 상세 정보  |
| /movie_board/{article_pk}/edit/   |PUT| 영화 게시판 게시글 수정  |
| /movie_board/{article_pk}/edit/   |delete| 영화 게시판 게시글 삭제  |
| /movie_board/{article_pk}/comment/   |POST| 영화 게시판 댓글 작성  |
| /movie_board/{article_pk}/comment/{comment_pk}/   |PUT| 영화 게시판 댓글 수정  |
| /movie_board/{article_pk}/comment/{comment_pk}/   |delete| 영화 게시판 댓글 삭제  |
| /movie_board/{article_pk}/like/   |POST| 영화 게시판 게시글 좋아요  |

### 영화 API
|         URL       |Method  |            설명         |
| /movies/   |GET| 영화 리스트 조회  |
| /movies/filter-genre/{genre}/   |GET| 장르별 영화 조회  |
| /movies/filter-actor/{actor}/   |GET| 배우별 영화 조회  |
| /movies/emotion_recommend/{emotion}/   |GET| 기분 바탕 영화 리스트 조회 |
| /movies/personal_recommend/{movie_lst}   |GET| emotion_recommend 선택 영화 바탕으로 영화 리스트 조회(tmdb_smillar 사용) |
| /movies/personal_recommend/{movie_title}   |POST| GET 요청에서 선택한 영화 저장 |

## DB_모델

## MovieBoardArticle 모델

| Name       | Type           | Description             | DB Relationship       |
|------------|----------------|-------------------------|-----------------------|
| title      | CharField(50)  | 기사 제목               |                       |
| content    | CharField(500) | 기사 내용               |                       |
| created_at | DateTime       | 기사 생성 날짜          |                       |
| updated_at | DateTime       | 기사 수정 날짜          |                       |
| user       | Foreign Key    | 작성자                  | 사용자:기사 = 1:N     |
| like_user  | ManyToMany     | 좋아요 표시한 사용자    | 사용자:기사 = M:N     |
| movie      | Foreign Key    | 관련 영화               | 영화:기사 = 1:N       |

## MovieBoardComment 모델

| Name       | Type           | Description             | DB Relationship       |
|------------|----------------|-------------------------|-----------------------|
| article    | Foreign Key    | 관련 기사               | 기사:댓글 = 1:N       |
| userId     | Foreign Key    | 작성자                  | 사용자:댓글 = 1:N     |
| content    | TextField      | 댓글 내용               |                       |
| created_at | DateTime       | 댓글 생성 날짜          |                       |
| updated_at | DateTime       | 댓글 수정 날짜          |                       |

## FreeBoardArticle 모델

| Name       | Type           | Description             | DB Relationship       |
|------------|----------------|-------------------------|-----------------------|
| title      | CharField(50)  | 게시물 제목             |                       |
| content    | CharField(500) | 게시물 내용             |                       |
| created_at | DateTime       | 게시물 생성 날짜        |                       |
| updated_at | DateTime       | 게시물 수정 날짜        |                       |
| userId     | Foreign Key    | 작성자                  | 사용자:게시물 = 1:N   |
| like_user  | ManyToMany     | 좋아요 표시한 사용자    | 사용자:게시물 = M:N   |

## FreeBoardComment 모델

| Name       | Type           | Description             | DB Relationship       |
|------------|----------------|-------------------------|-----------------------|
| article    | Foreign Key    | 관련 게시물             | 게시물:댓글 = 1:N     |
| userId     | Foreign Key    | 작성자                  | 사용자:댓글 = 1:N     |
| content    | TextField      | 댓글 내용               |                       |
| created_at | DateTime       | 댓글 생성 날짜          |                       |
| updated_at | DateTime       | 댓글 수정 날짜          |                       |

## Genre 모델

| Name | Type          | Description | DB Relationship |
|------|---------------|--------------|-----------------|
| name | CharField(20) | 장르 이름    |                 |

## Movie 모델

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
| liked_user   | Foreign Key    | 좋아요 표시한 사용자    | 사용자:영화 = 1:N     |