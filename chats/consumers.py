from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from .models import PrivateChatRoom, GroupChatRoom, Chats, User

class ChatConsumer(AsyncJsonWebsocketConsumer):
    
    # WebSocket 연결 시 실행
    async def connect(self):
        try:
            # URL에서 room_id를 가져오고, room_id가 없으면 None으로 설정
            self.room_id = self.scope['url_route']['kwargs'].get('room_id', None)
            
            # 방 ID가 있을 경우
            if self.room_id:  
                if not await self.check_room_exists(self.room_id):  # 방이 존재하는지 확인
                    raise ValueError('채팅방이 존재하지 않습니다.')  # 없으면 오류 발생
                self.group_name = self.get_group_name(self.room_id)  # 방 ID로 그룹 이름 생성
            
            # 개인 채팅일 경우
            else:  
                self.group_name = await self.create_or_get_private_room()  # 개인 채팅방 생성

            # WebSocket 그룹에 현재 사용자를 추가하고 연결 수락
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()

        except ValueError as e:
            # 방이 없거나 오류가 발생하면 오류 메시지를 보내고 연결 종료
            await self.send_json({'error': str(e)})
            await self.close()

    # WebSocket 연결 종료 시 실행되는 함수
    async def disconnect(self, close_code):
        try:
            # 그룹에서 현재 사용자(채널) 제거
            await self.channel_layer.group_discard(self.group_name, self.channel_name)
        except Exception as e:
            pass

    # 메시지 보낼 때 실행되는 함수
    async def receive_json(self, content):
        try:
            # 클라이언트에게 받은 데이터 > 변수로 추출
            message = content['message']  # 메시지 내용
            sender_email = content['sender_email']  # 발신자 이메일

            # 메시지 데이터베이스에 저장
            await self.save_message(self.room_id, sender_email, message)

            # 단톡에 메시지 전송 (다른 모든 사용자에게 전달)
            await self.channel_layer.group_send(self.group_name, {
                'type': 'chat_message',
                'message': message,
                'sender_email': sender_email
            })

        except ValueError as e:
            # 오류가 있을 경우 오류 메시지 전송
            await self.send_json({'error': str(e)})

    # 그룹 내의 다른 유저가 메시지를 보냈을 때, 그 메시지를 받은 클라이언트 측에서 실행되는 함수
    async def chat_message(self, event):
        message = event['message']  # 전송된 메시지
        sender_email = event['sender_email']  # 발신자 이메일
        # 클라이언트로 메시지와 발신자 정보를 다시 보냄
        await self.send_json({
            'message': message,
            'sender_email': sender_email
        })

    # 채팅방 ID로 WebSocket 그룹 이름 생성
    @staticmethod
    def get_group_name(room_id):
        return f"chat_room_{room_id}"  # "chat_room_<room_id>" 형식으로 그룹 이름 생성

    # 데이터베이스에서 해당 방이 존재하는지 확인
    @database_sync_to_async
    def check_room_exists(self, room_id):
        # 방이 존재하는지 확인, PrivateChatRoom이나 GroupChatRoom 사용 가능
        return PrivateChatRoom.objects.filter(id=room_id).exists() or GroupChatRoom.objects.filter(id=room_id).exists()

    # 메시지를 데이터베이스에 저장하는 함수
    @database_sync_to_async
    def save_message(self, room_id, sender_email, message):
        # 방이 Private 또는 Group에 있는지 확인 후 저장
        if PrivateChatRoom.objects.filter(id=room_id).exists():
            room = PrivateChatRoom.objects.get(id=room_id)
            Chats.objects.create(private_room=room, sender=User.objects.get(email=sender_email), content=message)
        elif GroupChatRoom.objects.filter(id=room_id).exists():
            room = GroupChatRoom.objects.get(id=room_id)
            Chats.objects.create(chat_room=room, sender=User.objects.get(email=sender_email), content=message)

    # 개인 채팅 방을 생성하거나 가져오는 함수
    @database_sync_to_async
    def create_or_get_private_room(self):
        # 개인 채팅의 사용자 이메일을 URL에서 추출
        user1_email = self.scope['url_route']['kwargs']['user1_email']
        user2_email = self.scope['url_route']['kwargs']['user2_email']

        # 각 사용자가 데이터베이스에 있는지 확인하고 없으면 생성
        user1 = User.objects.get(email=user1_email)
        user2 = User.objects.get(email=user2_email)

        # 두 사용자에 대해 채팅 방을 생성하거나 가져오기
        room, _ = PrivateChatRoom.objects.get_or_create(user1=user1, user2=user2)
        return self.get_group_name(room.id)  # 방 ID로 그룹 이름 반환

    # 단체 채팅방을 생성하거나 가져오는 함수
    @database_sync_to_async
    def create_group_chat(self, user_list, room_name=None):
        if not room_name:  # 방장이 이름을 지정하지 않았을 때
            room_name = '_'.join([user.username for user in user_list])  # 유저 이름으로 방 이름 생성

        # 방을 생성하거나 존재하는 방 가져오기
        room, created = GroupChatRoom.objects.get_or_create(name=room_name)
        return room.id  # 방 ID 반환
