import openai
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from .models import PrivateChatRoom, Message
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

# OpenAI API 설정
openai.api_key = settings.OPENAI_API_KEY  # settings.py에서 API 키 가져오기

# 욕설 및 공격적인 발언 감지 함수
def detect_profanity_and_aggression(message):
    prompt = (f"상대방의 마음을 상하게 하는 다양한 언어 표현을 걸러야 합니다. "
              f"예를 들어 '너 엄마는 있냐?' 같은 말은 단순한 질문이 아니라, 상대방에게 "
              f"엄마 없이 자랐냐는 뉘앙스를 줘서 마음을 상하게 하는 말입니다. "
              f"다음 메시지가 공격적이거나 상대방을 상처 줄 수 있는 말인지 확인해주세요: '{message}'")

    response = openai.Completion.create(
        engine="gpt-3.5-turbo",
        prompt=prompt,
        max_tokens=10,
        n=1,
        stop=None,
        temperature=0.5,
    )
    
    result = response.choices[0].text.strip().lower()
    if 'yes' in result:
        return True
    return False

class ChatConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        try:
            self.room_id = self.scope['url_route']['kwargs']['room_id']  # URL 경로에서 방 ID 추출

            # 방 존재 여부 확인
            if not await self.check_room_exists(self.room_id):
                raise ValueError('채팅방이 존재하지 않습니다.')

            group_name = self.get_group_name(self.room_id)  # 그룹 이름 생성

            # 그룹에 추가 후 WebSocket 연결 수락
            await self.channel_layer.group_add(group_name, self.channel_name)                 
            await self.accept()

        except ValueError as e:
            await self.send_json({'error': str(e)})
            await self.close()

    async def disconnect(self, close_code):
        # 그룹에서 제거
        group_name = self.get_group_name(self.room_id)
        await self.channel_layer.group_discard(group_name, self.channel_name)

    async def receive_json(self, content):
        try:
            message = content.get('message')
            sender_username = content.get('sender_username')
            user1_username = content.get('user1_username')
            user2_username = content.get('user2_username')

            # 필수 데이터 확인
            if not user1_username or not user2_username:
                raise ValueError("유저1과 유저2의 유저네임이 필요합니다.")

            # OpenAI API로 메시지가 공격적인지 확인
            is_profanity = await database_sync_to_async(detect_profanity_and_aggression)(message)
            if is_profanity:
                await self.send_json({
                    'error': '공격적이거나 상대방에게 상처를 줄 수 있는 메시지입니다. 다시 입력해주세요.'
                })
                return

            # 방을 가져오거나 생성
            room = await self.get_or_create_room(user1_username, user2_username)
            self.room_id = str(room.id)

            # 메시지 저장
            await self.save_message(room, sender_username, message)

            # 그룹에 메시지 전송
            group_name = self.get_group_name(self.room_id)
            await self.channel_layer.group_send(group_name, {
                'type': 'chat_message',
                'message': message,
                'sender_username': sender_username 
            })

        except ValueError as e:
            await self.send_json({'error': str(e)})

    async def chat_message(self, event):
        try:
            message = event['message']
            sender_username = event['sender_username']
            await self.send_json({'message': message, 'sender_username': sender_username})

        except Exception as e:
            await self.send_json({'error': f'메시지 전송 실패: {str(e)}'})

    @staticmethod
    def get_group_name(room_id):
        return f"chat_room_{room_id}"

    @database_sync_to_async
    def get_or_create_room(self, user1_username, user2_username):
        user1, _ = User.objects.get_or_create(username=user1_username)
        user2, _ = User.objects.get_or_create(username=user2_username)

        room, created = PrivateChatRoom.objects.get_or_create(user1=user1, user2=user2)
        return room

    @database_sync_to_async
    def save_message(self, room, sender_username, message_text):
        # 발신자 username과 메시지 텍스트 확인 후 저장
        sender = User.objects.get(username=sender_username)
        Message.objects.create(room=room, sender=sender, text=message_text)

    @database_sync_to_async
    def check_room_exists(self, room_id):
        return PrivateChatRoom.objects.filter(id=room_id).exists()
