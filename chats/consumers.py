import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # 방 그룹 가입
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # 방 그룹에서 탈퇴
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # LLM으로 비속어 체크
        if await self.is_profanity(message):
            # 비속어가 포함된 경우 경고 메시지를 보내고 그룹 메시지 전송 중단
            await self.send(text_data=json.dumps({
                'message': '🚫경고: 나쁜말이 감지되었어요🥲 예쁜말을 사용해야죠💓'
            }))
        else:
            # 방 그룹에 메시지 전송 (비속어가 아닌 경우)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message
                }
            )

    async def chat_message(self, event):
        message = event['message']
        # 웹소켓에 메시지 전송
        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def is_profanity(self, message):
        """
        LLM 사용
        프롬프트 엔지니어링
        """
        # LLM 코드
     
        if "비속어" in message: 
            return True
        return False
