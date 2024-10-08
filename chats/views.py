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
from .models import PrivateChatRoom, GroupChatRoom, RoomUsers
from .serializers import PrivateChatRoomSerializer, GroupChatRoomSerializer
from rest_framework import permissions


# class NotificationListView(ListAPIView):
#     serializer_class = NotificationSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return Notification.objects.filter(user=self.request.user, is_read=False).order_by('-pk')


# class ReportsViewSet(viewsets.ModelViewSet):
#     queryset = Reports.objects.all()
#     serializer_class = ReportsSerializer

#     def send_warning_message(self, reported_user, chat):
#         warning_message = textwrap.dedent(f"""
#         {reported_user}님 10번이나 나쁜말을 사용하셨네요🥲 화나는 일이 있으셨나요?
#         예쁜 말 고운 말을 쓸 수 있게 하루동안 wp.gg가 도와드릴게요! 채팅 속도가 미세하게 느려질 수 있습니다!
#         """)
#         Notification.objects.create(
#             user=reported_user,
#             chat=chat,
#             message=warning_message,
#             is_read=False
#         )

#     def perform_create(self, serializer):
#         report = serializer.save()
#         self.send_warning_message(report.reported, report.chat)
#         self.apply_llm_moderation()

#     def apply_llm_moderation(self):
#         """LLM 적용 예정"""
#         pass

def index(request):
    return render(request, "chat/index.html")

class ChatRoomListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
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