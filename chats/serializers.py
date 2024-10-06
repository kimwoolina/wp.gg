from rest_framework import serializers
from .models import Notification, Chats, Reports, Message, PrivateChatRoom, GroupChat, GroupChatMessage


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['chat_private', 'chat_group', 'is_read', 'created_at'] 

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.chat_private:
            data['message'] = f'{instance.chat_private.user2}님이 메시지를 보냈어요💌'
        elif instance.chat_group:
            data['message'] = f'{instance.chat_group.room_name}에서 새로운 메시지가 있습니다📩'
        else:
            data['message'] = '새로운 알림이 있어요📩'
        return data


class ChatsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chats
        fields = ['sender', 'content', 'is_read', 'created_at']

    def filter_profanity(self, content):
        """금지어 필터링 및 치환"""
        profanity_list = [
        "바보", "병신", "ㅂㅅ", "ㅅㅂ", "씨발", "시발", "개새끼", "ㄱㅅㄲ", "쓰레기", "좆", "미친", 
        "미천놈","나쁜놈", "싸가지", "대가리", "씹", "지랄", "엿먹어", "바퀴벌레", "찌질이", "애미", "애비", 
        "새끼", "새꺄", "ㅆ", "역겹", "ㅅㄲ", "정신병", "겁쟁이", "창녀", "썅", "빡대가리", "개같은", "병자", 
        "염병", "이따위", "인생망", "찌질", "한심", "새끼", "쌍놈", "그지", "똥", "거지", "하수구", "노무", 
        "개소리", "존나", "ㅈㄴ", "넌뭐임", "ㄲㅈ", "바퀴벌레", "후레자식", "벌레새끼", "ㅗ", "망", "죽을래", "뒤질래"
        ]
        for word in profanity_list:
            content = content.replace(word, '🫣🫣')
        return content

    def create(self, validated_data):
        validated_data['content'] = self.filter_profanity(validated_data.get('content', ''))
        return super().create(validated_data)


class ReportsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reports
        fields = ['chat', 'reporter', 'reported', 'content']


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ('sender', 'content', 'timestamp')


class ChatRoomSerializer(serializers.ModelSerializer):
    latest_message = serializers.SerializerMethodField()
    opponent_username = serializers.SerializerMethodField()
    messages = serializers.SerializerMethodField()

    class Meta:
        model = PrivateChatRoom
        fields = ['room_name', 'user1', 'user2', 'latest_message', 'opponent_username', 'messages']

    def get_latest_message(self, obj):
        latest_msg = Message.objects.filter(room=obj).order_by('-timestamp').first()
        return latest_msg.text if latest_msg else None

    def get_opponent_username(self, obj):
        request_user = self.context['request'].user
        if request_user == obj.user1:
            return obj.user2.username
        return obj.user1.username

    def get_messages(self, obj):
        messages = Message.objects.filter(room=obj).order_by('timestamp')
        return MessageSerializer(messages, many=True).data
    

class GroupChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupChat
        fields = ['username', 'roomname', 'members']


class GroupChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupChatMessage
        fields = ['username', 'group_chat', 'sender', 'content', 'timestamp']
