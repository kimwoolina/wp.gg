from rest_framework import generics, serializers, status
from rest_framework.response import Response
from .models import PrivateChatRoom, Message, User, GroupChat, GroupChatMessage
from .serializers import ChatRoomSerializer, MessageSerializer, GroupChatSerializer, GroupChatMessageSerializer
from rest_framework.exceptions import ValidationError
from django.http import Http404
from django.views.generic import TemplateView 
from rest_framework.permissions import IsAuthenticated


# 채팅방 목록 조회 및 생성
class ChatRoomListCreateView(generics.ListCreateAPIView):
    serializer_class = ChatRoomSerializer

    def get_queryset(self):
        user_username = self.request.query_params.get('username', None)

        if not user_username:
            raise ValidationError('username 파라미터가 필요합니다.')

        return PrivateChatRoom.objects.filter(
            user1__username=user_username
        ) | PrivateChatRoom.objects.filter(
            user2__username=user_username
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_create(self, serializer):
        user1_username = self.request.data.get('user1_username')
        user2_username = self.request.data.get('user2_username')

        # 유저1, 유저2가 존재하는지 확인
        user1 = User.objects.filter(username=user1_username).first()
        user2 = User.objects.filter(username=user2_username).first()

        if not user1:
            raise ValidationError(f'{user1_username}님이 존재하지 않습니다.')
        if not user2:
            raise ValidationError(f'{user2_username}님이 존재하지 않습니다.')

        # 이미 존재하는 채팅방이 있는지 확인하고, 있으면 반환
        chat_room, created = PrivateChatRoom.objects.get_or_create(user1=user1, user2=user2)
        if not created:
            # 이미 존재하는 채팅방을 반환
            return Response(ChatRoomSerializer(chat_room).data, status=status.HTTP_200_OK)

        # 새로운 채팅방 생성
        serializer.save(user1=user1, user2=user2)


# 메시지 목록 조회
class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        room_id = self.kwargs.get('room_id')
        
        if not room_id:
            raise ValidationError({'detail': 'room_id 파라미터가 필요합니다.'})

        queryset = Message.objects.filter(room_id=room_id)

        if not queryset.exists():
            raise Http404('해당 room_id로 메시지를 찾을 수 없습니다.')

        return queryset


class GroupChatListCreateView(generics.ListCreateAPIView):
    queryset = GroupChat.objects.all()
    serializer_class = GroupChatSerializer


class GroupChatMessageListView(generics.ListCreateAPIView):
    queryset = GroupChatMessage.objects.all()
    serializer_class = GroupChatMessageSerializer

    def get_queryset(self):
        group_chat_id = self.kwargs['group_chat_id']
        return self.queryset.filter(group_chat__id=group_chat_id)


class ChatTemplateView(TemplateView):  
    template_name = 'chat.html' 


class SendMessageView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        receiver_username = self.kwargs['username']  # URL에서 유저네임 가져오기
        try:
            receiver = User.objects.get(username=receiver_username)
        except User.DoesNotExist:
            raise ValidationError(f'User with username {receiver_username} does not exist.')

        # 1:1 채팅방 가져오기 (없으면 생성)
        chat_room, created = PrivateChatRoom.objects.get_or_create(user1=self.request.user, user2=receiver)

        # 메시지 저장
        serializer.save(room=chat_room, sender=self.request.user)

