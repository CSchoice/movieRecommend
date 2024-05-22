from decouple import config
import requests
import json

url = f"https://api.themoviedb.org/3/movie/74849?language=ko-KR"

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {config('TMDB_KEY')}"
}

response = requests.get(url, headers=headers)
print(response.json())