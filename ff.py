import requests

url = "https://api.themoviedb.org/3/movie/1022789?language=en-US"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5NzBmZjQxMDZkN2M3NWQ4YThiMDYwNzhlMzUxMjgwZiIsInN1YiI6IjY2Mjc0MzliYWY5NTkwMDE2NDY5MzQ5MiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.JAyRCq0NoCjWHtBG6mp5xtIMvf5gpqgJTg_7S-SGTa0"
}

response = requests.get(url, headers=headers)

print(response.text)