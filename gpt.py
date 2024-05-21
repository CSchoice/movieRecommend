import openai
import requests

# API 키 설정
OPENAI_API_KEY = 'sk-proj-Vg67oj0tLNOVqO4HeyoJT3BlbkFJHOSZXr9VRLoPofam5kd9'
TMDB_API_KEY = '970ff4106d7c75d8a8b06078e351280f'

openai.api_key = OPENAI_API_KEY

def recommend_highly_rated_similar_movies(emotion, movie_title):
    prompt = (
        f"The user is currently feeling '{emotion}'."
        f"The user liked the movie '{movie_title}'."
        f"Recommend movies that are similar to this and have a rating of 9 out of 10 or higher."
        f"Include detailed descriptions for each movie."
        f"Recommend movies from the 2010s or later."
        f"answer Korean response"
        f"based on emotion 70%, movie_title 30%"
    )
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a movie critic and helpful assistant ."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=700
    )
    recommended_movies = response.choices[0].message['content'].strip()
    return recommended_movies

def main():
    emotion = input("감정을 입력하세요 (화남, 슬픔, 따분함, 행복): ")
    movie_title = input("좋아하는 영화 제목을 입력하세요: ")
    recommendations = recommend_highly_rated_similar_movies(emotion, movie_title)
    print(f"\n'{movie_title}'와(과) 유사한 영화 추천 목록:\n{recommendations}")

main()