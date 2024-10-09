from django.db import models
import uuid
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

# 1:1 개인 채팅방
class PrivateChatRoom(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='private_room_user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='private_room_user2')
    room_name = models.CharField(max_length=15, blank=True, null=True)
    room_image = models.ImageField(upload_to='room_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # 장고 3.2 이상부터는 unique_together보다 UniqueConstraint이 권장된다고 함
        constraints = [
            models.UniqueConstraint(fields=['user1', 'user2'], name='unique_private_chatroom') 
        ]

    def save(self, *args, **kwargs):
        # 방 이름 없으면 user2의 유저네임으로 설정
        if not self.room_name:
            self.room_name = self.user2.username
        super().save(*args, **kwargs)

    def get_latest_message(self):
        return self.messages.order_by('-created_at').first()
    
    def __str__(self):
        return f'1:1 채팅방: {self.user1.username}님과 {self.user2.username}님'


# 단체 채팅방
class GroupChatRoom(models.Model):
    owner = models.ForeignKey(User, related_name='owned_group_chats', on_delete=models.CASCADE)  # 방장
    room_name = models.CharField(max_length=15)
    room_image = models.ImageField(upload_to='room_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_latest_message(self):
        return GroupChatMessage.objects.filter(group_chat=self).order_by('-created_at').first()
    
    def __str__(self):
        return f'단체 채팅방: {self.room_name} (방장: {self.owner.username})'


# 1:1 개인 채팅 저장
class ChatMessage(models.Model):
    room = models.ForeignKey(PrivateChatRoom, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")  # 발신자
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def mark_as_read(self):
        self.is_read = True
        self.save()

    def __str__(self):
        return f'{self.sender.username}: {self.content[:10]}'  # 첫 10자만 표시


# 그룹 채팅 저장
class RoomUsers(models.Model):
    group_chat = models.ForeignKey(GroupChatRoom, on_delete=models.CASCADE, related_name='room_users')  # 그룹 채팅 FK
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 그룹에 속한 유저


class GroupChatMessage(models.Model):
    group_chat = models.ForeignKey(GroupChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)  # 메시지를 보낸 유저
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def mark_as_read(self):
        self.is_read = True
        self.save()

    def __str__(self):
        return f"{self.sender.username}: {self.content[:20]}"
    

# 신고
class Reports(models.Model):
    chat_private = models.ForeignKey(PrivateChatRoom, on_delete=models.CASCADE, null=True, blank=True)
    chat_group = models.ForeignKey(GroupChatRoom, on_delete=models.CASCADE, null=True, blank=True)
    reporter = models.ForeignKey(User, related_name='reports_made', on_delete=models.CASCADE)
    reported = models.ForeignKey(User, related_name='reports_received', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # 본인 신고 못하게, 중복 신고 금지 필요
    
    def __str__(self):
        return f'{self.reporter}님이 {self.reported}님을 신고함. 사유: {self.content}'


# 알림
class Notification(models.Model):
    # notification_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # user FK
    chat_private = models.ForeignKey(PrivateChatRoom, on_delete=models.CASCADE, null=True, blank=True)
    chat_group = models.ForeignKey(GroupChatRoom, on_delete=models.CASCADE, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}님에게 온 새로운 메시지: {self.chat}'  # chat의 __str__ 메서드 사용 > 메시지 자동 생성
