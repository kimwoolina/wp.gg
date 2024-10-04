from django.shortcuts import render
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework import viewsets, generics, serializers, status
from .models import Notification, Reports, Message, Chats, PrivateChatRoom, GroupChatRoom
from .serializers import NotificationSerializer, ReportsSerializer, MessageSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django.http import Http404
import textwrap
from rest_framework.response import Response

# 알림 목록을 조회
class NotificationListView(ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """현재 로그인한 사용자에게 할당된 읽지 않은 알림을 반환"""
        return Notification.objects.filter(user=self.request.user, is_read=False).order_by('-pk')


# 신고 
class ReportsViewSet(viewsets.ModelViewSet):
    queryset = Reports.objects.all()
    serializer_class = ReportsSerializer

    def send_warning_message(self, reported_user, chat=None):
        """10번 이상 신고된 사용자에게 경고 메시지 전송"""
        warning_message = textwrap.dedent(f"""
        {reported_user}님 10번이나 나쁜말을 사용하셨네요🥲 화나는 일이 있으셨나요?
        예쁜 말 고운 말을 쓸 수 있게 하루동안 wp.gg가 도와드릴게요! 채팅 속도가 미세하게 느려질 수 있습니다!
        """)
        
        Notification.objects.create(
            user=reported_user,
            message=warning_message,
            is_read=False
        )

    def perform_create(self, serializer):
        """신고 생성 후 경고 메시지 전송"""
        report = serializer.save()
        self.send_warning_message(report.reported, getattr(report, 'chat', None))
        self.apply_llm_moderation()

    def apply_llm_moderation(self):
        """LLM 적용"""
        pass


# 메시지 목록 조회 및 생성
class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        room_id = self.kwargs.get('room_id')  # URL에서 room_id 가져오기
        if not room_id:
            # room_id가 제공되지 않은 경우, 400 반환
            return Response({'detail': 'room_id 파라미터가 필요합니다.'}, status=status.HTTP_400_BAD_REQUEST)

        # 주어진 room_id에 해당하는 메시지 쿼리셋 필터링
        queryset = Message.objects.filter(room_id=room_id)
        if not queryset.exists():
            # 해당 room_id로 메시지를 찾을 수 없는 경우, 404 반환
            return Response({'detail': '해당 room_id로 메시지를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        
        # 필터링된 메시지 쿼리셋 반환
        return queryset  

    def create(self, request, *args, **kwargs):
        # 요청 데이터로부터 serializer 인스턴스 생성
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            # serializer가 유효하지 않은 경우, 오류 메시지를 포함한 400 반환
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        room_id = self.kwargs.get('room_id')  # URL에서 room_id 가져오기
        
        # 주어진 room_id에 해당하는 채팅방이 존재하는지 확인
        if not PrivateChatRoom.objects.filter(id=room_id).exists() and not GroupChatRoom.objects.filter(id=room_id).exists():
            # 채팅방이 존재하지 않는 경우, 404 반환
            return Response({'detail': '해당 채팅방이 존재하지 않습니다.'}, status=status.HTTP_404_NOT_FOUND)

        # 메시지를 데이터베이스에 저장
        self.perform_create(serializer)
         # 생성된 메시지 데이터와 함께 201 반환
        return Response(serializer.data, status=status.HTTP_201_CREATED) 

    def perform_create(self, serializer):
        room_id = self.kwargs.get('room_id')  # URL에서 room_id 가져오기


# 채팅 앱 인덱스 페이지
def index(request):
    return render(request, "chat/index.html")
