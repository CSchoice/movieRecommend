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
        {"role": "user", "content": '사용자가 입력한 감정을 해소할 수 있는 장르를 3개 추천해주고, 그 장르를 바탕으로 영화를 10개 추천해줘, 그리고 영화 포스터 이미지를 구글에서 찾아서 보여줘'},
        {"role": "user", "content": '그 영화들의 포스터 이미지를 같이 보내줘'},
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
        print(f"추천 영화: {recommendation}")

# 챗봇 실행
chatbot()