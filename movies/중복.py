
import json


with open('movies/data/movie_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

ids = [item["id"] for item in data]
duplicate_ids = set([x for x in ids if ids.count(x) > 1])

print("중복된 id 값:", duplicate_ids)