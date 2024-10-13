from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework import viewsets
from .models import Notification, Reports
# from .serializers import NotificationSerializer, ReportsSerializer
from rest_framework.permissions import IsAuthenticated
import textwrap
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from itertools import chain
from operator import attrgetter
from .models import PrivateChatRoom, GroupChatRoom, RoomUsers, ChatMessage, GroupChatMessage
from .serializers import PrivateChatRoomSerializer, GroupChatRoomSerializer, ChatMessageSerializer, GroupChatMessageSerializer
from rest_framework import permissions
from rest_framework import status
from rest_framework import generics
from django.contrib.auth import get_user_model
from django.views import generic

User = get_user_model()

# def index(request):
#     return render(request, "chats/index.html")

# 개인 채팅방 생성
class PrivateChatRoomCreateView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        user2_id = request.data.get('user2')  # user2 ID를 가져옴
        if not user2_id:
            return Response({"error": "user2 ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        # 개인 채팅방 생성
        private_chat_room = PrivateChatRoom(user1=request.user, user2_id=user2_id)
        private_chat_room.save()

        serializer = PrivateChatRoomSerializer(private_chat_room)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    
class PrivateChatRoomListView(APIView):
    # permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능

    def get(self, request):
        user = request.user
        # 현재 사용자가 참여한 개인 채팅방 필터링 및 생성일 기준으로 내림차순 정렬
        chat_rooms = PrivateChatRoom.objects.filter(user1=user) | PrivateChatRoom.objects.filter(user2=user)
        chat_rooms = chat_rooms.order_by('-created_at')  # 생성일 기준 내림차순 정렬
        serializer = PrivateChatRoomSerializer(chat_rooms, many=True)  # 직렬화
        return Response(serializer.data)  


# 개인 메시지 리스트
class PrivateChatMessageList(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, room_id, *args, **kwargs):  # room_id를 URL 경로에서 직접 받기
        if not room_id:
            return Response({"error": "room_id parameter is required"}, status=400)

        try:
            room = PrivateChatRoom.objects.get(id=room_id)
        except PrivateChatRoom.DoesNotExist:
            return Response({"error": "Chat room not found"}, status=404)

        messages = ChatMessage.objects.filter(room=room)
        serializer = ChatMessageSerializer(messages, many=True)
        return Response(serializer.data)


    
# 개인 메시지 전송
class PrivateChatMessageCreate(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data
        room_id = data.get('room_id')
        content = data.get('content')

        if not room_id or not content:
            return Response({"error": "room_id and content are required"}, status=400)

        try:
            room = PrivateChatRoom.objects.get(id=room_id)
        except PrivateChatRoom.DoesNotExist:
            return Response({"error": "Chat room not found"}, status=404)

        message = ChatMessage.objects.create(
            room=room,
            sender=request.user,
            content=content
        )
        serializer = ChatMessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
# 채팅방 템플릿 뷰
class ChatRoomTemplateView(generic.TemplateView):
    template_name = 'chats/chat.html'
    
# class ChatRoomTemplateView(APIView):
#     def get(self, request):
#         return render(request, 'chats/chat.html', {'user': request.user})
    
    

# 그룹 채팅방 생성
class GroupChatRoomCreateView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        room_name = request.data.get('room_name')
        if not room_name:
            return Response({"error": "room_name is required."}, status=status.HTTP_400_BAD_REQUEST)

        # 그룹 채팅방 생성
        group_chat_room = GroupChatRoom(owner=request.user, room_name=room_name)
        group_chat_room.save()

        serializer = GroupChatRoomSerializer(group_chat_room)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        
        
# 그룹 메시지 리스트
class GroupChatMessageList(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        group_chat_id = request.query_params.get('group_chat_id')  # 쿼리 파라미터에서 group_chat_id 받음
        if not group_chat_id:
            return Response({"error": "group_chat_id parameter is required"}, status=400)

        try:
            group_chat = GroupChatRoom.objects.get(id=group_chat_id)
        except GroupChatRoom.DoesNotExist:
            return Response({"error": "Group chat room not found"}, status=404)

        messages = GroupChatMessage.objects.filter(group_chat=group_chat)
        serializer = GroupChatMessageSerializer(messages, many=True)
        return Response(serializer.data)
    

class GroupChatMessageCreate(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data
        group_chat_id = data.get('group_chat_id')
        content = data.get('content')

        if not group_chat_id or not content:
            return Response({"error": "group_chat_id and content are required"}, status=400)

        try:
            group_chat = GroupChatRoom.objects.get(id=group_chat_id)
        except GroupChatRoom.DoesNotExist:
            return Response({"error": "Group chat room not found"}, status=404)

        message = GroupChatMessage.objects.create(
            group_chat=group_chat,
            sender=request.user,
            content=content
        )
        serializer = ChatMessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

# 개인+그룹 채팅방 목록 출력
class ChatRoomListView(APIView):
    """
    채팅방 목록 기능
    - 채팅방 최근 메시지 기준으로 정렬
    - 최근 메시지가 없을 경우 방 생성일로 정렬
    - 개인채팅방과 그룹채팅방을 함께 정렬
    
    작성자: 김우린
    작성 날짜: 2024.10.01
    """
    
    # permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        user = request.user  # 현재 로그인된 사용자

        # 프라이빗 채팅방 필터링 (user1 또는 user2인 경우)
        private_rooms = PrivateChatRoom.objects.filter(
            Q(user1=user) | Q(user2=user)
        )

        # 그룹 채팅방 필터링 (현재 사용자가 방장 또는 멤버인 경우)
        group_rooms_as_owner = GroupChatRoom.objects.filter(owner=user)
        group_rooms_as_member = RoomUsers.objects.filter(user=user).values_list('group_chat', flat=True)
        group_rooms = GroupChatRoom.objects.filter(id__in=group_rooms_as_member) | group_rooms_as_owner

        # 시리얼라이저로 직렬화
        private_serializer = PrivateChatRoomSerializer(private_rooms, many=True)
        group_serializer = GroupChatRoomSerializer(group_rooms, many=True)

        # 모든 채팅방을 리스트로 합치기
        chat_rooms = private_serializer.data + group_serializer.data

        # 최신 메시지의 생성일을 latest_created_at에 저장
        for room in chat_rooms:
            if room['latest_message']:
                room['latest_created_at'] = room['latest_message']['created_at']
            else:
                room['latest_created_at'] = room['created_at']  # 메시지가 없으면 방 생성일 사용

        # 최신 생성일 기준으로 정렬 (내림차순)
        chat_rooms.sort(key=lambda x: x['latest_created_at'], reverse=True)

        return Response({'chat_rooms': chat_rooms})
    