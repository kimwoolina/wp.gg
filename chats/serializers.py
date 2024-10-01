from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'chat', 'is_read', 'created_at']

    def to_representation(self, instance):
        """알림 메시지 형식"""
        data = super().to_representation(instance)
        if instance.chat:
            data['message'] = f'{instance.chat.sender}님이 {instance.chat.receiver}님에게 메시지를 보냈어요💌'
        else:
            data['message'] = '새로운 알림이 있어요📩'
        return data
