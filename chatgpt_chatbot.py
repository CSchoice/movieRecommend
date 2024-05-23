import json
import openai
from decouple import config

# API 키 설정
openai.api_key = config('GPT_KEY')
TMDB_API_KEY = '970ff4106d7c75d8a8b06078e351280f'

def get_movie_recommendation(messages):
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=700
    )
    return response.choices[0].message['content'].strip()

# 챗봇 루프
def chatbot():
    print("현재 기분에 따라 영화를 추천해 드립니다. 'exit'을 입력하면 대화가 종료됩니다.")
    
    messages = [
        {"role": "system", "content": "You are an expert in recommending movies and Korean."},
        {"role": "user", "content": "앞으로 답변은 한국어로 해줘"},
        {"role": "user", "content": "사용자가 입력한 감정을 해소할 수 있는 장르를 3개 추천해줘. (추천 장르는 보여주지 않아도 괜찮아)"},
        {"role": "user", "content": "앞에서 추천해준 장르별로 영화를 3개씩 추천해주고, 중복되지 않는 추가 추천 영화도 3개 추천해줘."},
        {"role": "user", "content": "12개의 영화를 |로 구분해서 []안에 담아줘."},
        {"role": "user", "content": "[]에 담긴 영화를 하나의 json 형식 만들어줘."}
    ]
    
    while True:
        user_input = input("지금 기분이 어떠신가요? (예: 기분이 우울해요): ")
        if user_input.lower() == "exit":
            print("챗봇을 종료합니다. 좋은 하루 되세요!")
            break
        
        # 사용자 입력을 messages 리스트에 추가
        messages.append({"role": "user", "content": user_input})
        
        # 영화 추천 받기
        recommendation = get_movie_recommendation(messages)
        
        # 챗봇의 응답을 messages 리스트에 추가
        messages.append({"role": "assistant", "content": recommendation})
        
        # 추천 영화 출력
        print(recommendation)
        recommendation = json.dumps(recommendation)
        # JSON 형식으로 변환하여 영화 제목 출력
        parsed_data = json.loads(recommendation)
        print(parsed_data)
        # movie_titles = parsed_data['movies']
        # for title in movie_titles:
        #     print(title)

# 챗봇 실행
chatbot()