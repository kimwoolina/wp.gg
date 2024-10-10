import openai
from django.conf import settings

openai.api_key = settings.OPEN_API_KEY

def ask_chatgpt(user_message, system_instructions):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_instructions},
                {"role": "user", "content": user_message}
            ],
        )
        
        # 응답에서 메시지 추출
        #return response.choices[0].message['content']
        return response['choices'][0]['message']['content']
    
    
    except Exception as e:
        return f"ChatGPT 요청 처리 오류: {str(e)}"
