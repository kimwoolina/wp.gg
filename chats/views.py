from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework import viewsets
from .models import Notification, Reports
from .serializers import NotificationSerializer, ReportsSerializer
from rest_framework.permissions import IsAuthenticated
import textwrap

class NotificationListView(ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user, is_read=False).order_by('-pk')


class ReportsViewSet(viewsets.ModelViewSet):
    queryset = Reports.objects.all()
    serializer_class = ReportsSerializer

    def send_warning_message(self, reported_user, chat):
        warning_message = textwrap.dedent(f"""
        {reported_user}님 10번이나 나쁜말을 사용하셨네요🥲 화나는 일이 있으셨나요?
        예쁜 말 고운 말을 쓸 수 있게 하루동안 wp.gg가 도와드릴게요! 채팅 속도가 미세하게 느려질 수 있습니다!
        """)
        Notification.objects.create(
            user=reported_user,
            chat=chat,
            message=warning_message,
            is_read=False
        )

    def perform_create(self, serializer):
        report = serializer.save()
        self.send_warning_message(report.reported, report.chat)
        self.apply_llm_moderation()

    def apply_llm_moderation(self):
        """LLM 적용 예정"""
        pass
