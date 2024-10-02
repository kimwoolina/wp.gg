import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async  
from .models import RoomUsers

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # URL에서 단톡방 이름 가져옴 
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        # 단톡방 이름 생성
        self.room_group_name = f'chat_{self.room_name}'

        # 단톡방에 현재 유저 추가
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        
        # 웹소켓 연결
        await self.accept()

    async def disconnect(self, close_code):
        # 현재 연결된 유저 가져오기
        user = self.scope['user'] 
        # 단톡방에서 유저 삭제
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        
        # 데이터베이스의 단톡방에서 유저 삭제 (비동기 호출)
        await sync_to_async(self.remove_user_from_room)(user, self.room.id, self.room_type)

    async def receive(self, text_data):
        # 클라이언트로부터 받은 메시지 처리
        text_data_json = json.loads(text_data)
        # 받은 메시지 추출
        message = text_data_json['message']  

        # 메시지가 비속어인지 확인 (비속어 필터링)
        if await self.is_profanity(message):
            # 비속어가 감지된 경우 경고 메시지를 보냄
            await self.send(text_data=json.dumps({
                'message': '🚫경고: 나쁜 말이 감지되었어요🥲 예쁜 말을 사용해야죠💓'
            }))
        else:
            # 비속어 아니면, 단톡에 메시지 전송
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message
                }
            )

    async def chat_message(self, event):
        # 단톡방에 전달받은 메시지 웹소켓으로 전송
        message = event['message']

        # 클라이언트에게 메시지 전송
        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def is_profanity(self, message):
        """
        LLM 비속어 감지
        """
        # 메시지에 비속어 있는지 확인
        if "비속어" in message: 
            return True
        return False
    def remove_user_from_room(user, room_id):
        """
        유저 단톡에서 제거하는 로직.
        - user: 채팅방에서 나가는 사용자
        - room_id: 사용자가 속해있던 단톡방 ID
        """
        try:
            # RoomUsers 테이블에서 room_id와 user_id가 일치하는 레코드 삭제
            room_user = RoomUsers.objects.get(room_id=room_id, user_id=user.id)
            # 단톡방에서 유저 삭제
            room_user.delete()  
            print(f"{user.username}님이 채팅방 {room_id}에서 나갔습니다👋")
        except RoomUsers.DoesNotExist:
            print(f"{user.username}님은 {room_id}에 없어요😂")
