from rest_framework import serializers
from .models import PrivateChatRoom, GroupChatRoom, ChatMessage, GroupChatMessage
from django.contrib.auth import get_user_model

User = get_user_model()

class SenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'profile_image']

class ChatMessageSerializer(serializers.ModelSerializer):
    sender = SenderSerializer() 
    
    class Meta:
        model = ChatMessage
        fields = ['sender', 'content', 'created_at', 'updated_at', 'is_read']


class PrivateChatRoomSerializer(serializers.ModelSerializer):
    latest_message = serializers.SerializerMethodField()

    class Meta:
        model = PrivateChatRoom
        fields = ['id', 'room_name', 'room_image', 'created_at', 'latest_message']

    def get_latest_message(self, obj):
        latest_message = obj.get_latest_message()
        if latest_message:
            return ChatMessageSerializer(latest_message).data  # 직렬화된 데이터 반환
        return None  # 메시지가 없는 경우 None 반환


class GroupChatMessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()  # 유저 이름을 문자열로 반환
    
    class Meta:
        model = GroupChatMessage
        fields = ['id', 'group_chat', 'sender', 'content', 'is_read', 'created_at', 'updated_at']
        
        
class GroupChatRoomSerializer(serializers.ModelSerializer):
    latest_message = serializers.SerializerMethodField()

    class Meta:
        model = GroupChatRoom
        fields = ['id', 'room_name', 'room_image', 'created_at', 'latest_message']

    def get_latest_message(self, obj):
        latest_message = obj.get_latest_message()
        if latest_message:
            return ChatMessageSerializer(latest_message).data  # 직렬화된 데이터 반환
        return None  # 메시지가 없는 경우 None 반환
