from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework import viewsets
from .models import Notification, Reports  # Notification 모델에 chat 필드가 있는지 확인 필요
from .serializers import NotificationSerializer, ReportsSerializer
from rest_framework.permissions import IsAuthenticated
import textwrap

class NotificationListView(ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """현재 로그인한 사용자에게 할당된 읽지 않은 알림을 반환"""
        return Notification.objects.filter(user=self.request.user, is_read=False).order_by('-pk')


class ReportsViewSet(viewsets.ModelViewSet):
    queryset = Reports.objects.all()
    serializer_class = ReportsSerializer

    def send_warning_message(self, reported_user, chat=None):
        """10번 이상 신고된 사용자에게 경고 메시지 전송"""
        warning_message = textwrap.dedent(f"""
        {reported_user}님 10번이나 나쁜말을 사용하셨네요🥲 화나는 일이 있으셨나요?
        예쁜 말 고운 말을 쓸 수 있게 하루동안 wp.gg가 도와드릴게요! 채팅 속도가 미세하게 느려질 수 있습니다!
        """)
        
        # Notification 생성 시 chat 필드가 필요 없으면 chat=None
        Notification.objects.create(
            user=reported_user,
            message=warning_message,
            is_read=False
        )

    def perform_create(self, serializer):
        """신고 생성 후 경고 메시지 전송"""
        report = serializer.save()
        # report.chat이 있을 경우에만 chat 전달 (필요 없는 경우 제거 가능)
        self.send_warning_message(report.reported, getattr(report, 'chat', None))
        self.apply_llm_moderation()

    def apply_llm_moderation(self):
        """LLM 적용을 위한 자리 표시자 메서드"""
        pass

def index(request):
    """채팅 애플리케이션 인덱스 페이지"""
    return render(request, "chat/index.html")
