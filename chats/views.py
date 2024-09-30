from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework.permissions import IsAuthenticated

class NotificationListView(ListAPIView):
    """특정 유저가 읽지 않은 알림 목록을 가져오는 API"""
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """현재 유저가 읽지 않은 알림을 조회"""
        return Notification.objects.filter(user=self.request.user, is_read=False).order_by('-pk')
