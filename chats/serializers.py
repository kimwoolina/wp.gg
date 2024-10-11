from rest_framework import serializers
from .models import PrivateChatRoom, GroupChatRoom, ChatMessage, GroupChatMessage
# from .models import Notification, Chats, Reports

# class NotificationSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = Notification
#         fields = ['id', 'chat', 'is_read', 'created_at', 'message'] 

#     def to_representation(self, instance):
#         data = super().to_representation(instance)
#         if instance.chat:
#             data['message'] = f'{instance.chat.sender}님이 {instance.chat.receiver}님에게 메시지를 보냈어요💌'
#         else:
#             data['message'] = instance.message or '새로운 알림이 있어요📩'  # message 필드 활용
#         return data

# class ChatsSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Chats
#         fields = ['sender', 'receiver', 'content', 'is_read', 'created_at']

#     def filter_profanity(self, content):
#         """금지어 필터링 및 치환"""
#         profanity_list = [
#         "바보", "병신", "ㅂㅅ", "ㅅㅂ", "씨발", "시발", "개새끼", "ㄱㅅㄲ", "쓰레기", "좆", "미친", 
#         "미천놈","나쁜놈", "싸가지", "대가리", "씹", "지랄", "엿먹어", "바퀴벌레", "찌질이", "애미", "애비", 
#         "새끼", "새꺄", "ㅆ", "역겹", "ㅅㄲ", "정신병", "겁쟁이", "창녀", "썅", "빡대가리", "개같은", "병자", 
#         "염병", "이따위", "인생망", "찌질", "한심", "새끼", "쌍놈", "그지", "똥", "거지", "하수구", "노무", 
#         "개소리", "존나", "ㅈㄴ", "넌뭐임", "ㄲㅈ", "바퀴벌레", "후레자식", "벌레새끼", "ㅗ", "망", "죽을래", "뒤질래"
#         ]
#         for word in profanity_list:
#             content = content.replace(word, '🫣🫣')
#         return content

#     def create(self, validated_data):
#         validated_data['content'] = self.filter_profanity(validated_data.get('content', ''))
#         return super().create(validated_data)


# class ReportsSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Reports
#         fields = ['chat', 'reporter', 'reported', 'content']

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['sender', 'content', 'created_at']


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

# class ChatRoomSerializer(serializers.Serializer):
#     room_id = serializers.UUIDField()
#     room_type = serializers.ChoiceField(choices=['private', 'group'])
#     room_name = serializers.CharField()
#     latest_message = serializers.CharField(allow_blank=True)
#     latest_sender = serializers.CharField(allow_blank=True)
#     created_at = serializers.DateTimeField()
