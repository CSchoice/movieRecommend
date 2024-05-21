import openai

# OpenAI API 키 설정
openai.api_key = 'sk-proj-Vg67oj0tLNOVqO4HeyoJT3BlbkFJHOSZXr9VRLoPofam5kd9'

def get_movie_recommendation(messages):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        max_tokens=700
    )
    return response.choices[0].message['content'].strip()

# 챗봇 루프
def chatbot():
    print("I will recommend a movie based on your current mood. Type 'exit' to end the conversation.")
    
    messages = [
        {"role": "system", "content": "You are an expert in recommending movies and Korean."}
    ]
    
    while True:
        user_input = input("How are you feeling right now? (e.g., I feel sad): ")
        if user_input.lower() == "exit":
            print("Ending the chatbot. Have a great day!")
            break
        
        # 사용자 입력을 messages 리스트에 추가
        messages.append({"role": "user", "content": user_input})
        
        # 영화 추천 받기
        recommendation = get_movie_recommendation(messages)
        
        # 챗봇의 응답을 messages 리스트에 추가
        messages.append({"role": "assistant", "content": recommendation})
        
        # 추천 영화 출력
        print(f"Recommended movie: {recommendation}")

# 챗봇 실행
chatbot()