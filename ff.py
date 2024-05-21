import requests

db_movie_id = 1022789

url = f"https://api.themoviedb.org/3/movie/{db_movie_id}?language=ko-KR"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer 970ff4106d7c75d8a8b06078e351280f"
    }

response = requests.get(url, headers=headers)

print(response.text, '--------------------------------')