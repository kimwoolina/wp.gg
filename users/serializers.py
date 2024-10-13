from .models import User
from rest_framework import serializers

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username', 
            'email', 
            'profile_image', 
            'platforms', 
            'riot_username', 
            'riot_tag', 
            'introduction', 
            'is_notification_sound_on',  # 알람 소리 설정
            'is_notification_message_on'  # 알람 메시지 설정
        ]
