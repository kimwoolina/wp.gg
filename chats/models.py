from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

# 1:1 개인 채팅방
class PrivateChatRoom(models.Model):
    user1 = models.ForeignKey(User, related_name='private_chats_initiated', on_delete=models.CASCADE)  # 채팅 신청한 유저
    user2 = models.ForeignKey(User, related_name='private_chats_received', on_delete=models.CASCADE)  # 채팅 신청받은 유저
    room_name = models.CharField(max_length=15, blank=True, null=True)  # 지정하지 않았다면 유저2의 이름으로
    room_image = models.ImageField(upload_to='room_images/', blank=True, null=True)  # 유저2의 프로필 이미지로 지정
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # 같은 유저 간 중복 허용 X
        unique_together = ('user1', 'user2')  

    def save(self, *args, **kwargs):
        # 방 이름이나 이미지가 지정되지 않으면 유저2의 이름과 유저2의 프로필 이미지로 설정
        if not self.room_name:
            self.room_name = self.user2.username
        super().save(*args, **kwargs)

    def __str__(self):
        return f'1:1 채팅방: {self.user1}님과 {self.user2}님'


# 단체 채팅방
class GroupChatRoom(models.Model):
    room_name = models.CharField(max_length=15)  # 단체 채팅방 이름
    room_image = models.ImageField(upload_to='room_images/', blank=True, null=True)  # 단체 채팅방 이미지
    owner = models.ForeignKey(User, related_name='owned_group_chats', on_delete=models.CASCADE)  # 방장
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'단체 채팅방: {self.room_name} (방장: {self.owner.username})'

# 중계 테이블 (RoomUsers)
class RoomUsers(models.Model):
    room = models.ForeignKey(GroupChatRoom, on_delete=models.CASCADE)  # 단체 채팅방 ID
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 참여하는 유저
    joined_at = models.DateTimeField(auto_now_add=True)

    # 같은 채팅방에 중복된 유저가 없도록 설정
    class Meta:
        unique_together = ('room', 'user')  

    def __str__(self):
        return f'{self.user.username}님이 {self.room.room_name}에 참여중'


class Chats(models.Model):
    chat_id = models.AutoField(primary_key=True)  # PK
    sender = models.ForeignKey(User, related_name='sent_chats', on_delete=models.CASCADE)  # 보낸 사람
    chat_room = models.ForeignKey(GroupChatRoom, related_name='group_chats', on_delete=models.CASCADE, null=True, blank=True)  # 단체 채팅방 시 사용
    private_room = models.ForeignKey(PrivateChatRoom, related_name='private_chats', on_delete=models.CASCADE, null=True, blank=True)  # 1:1 채팅방 시 사용
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def mark_as_read(self):
        self.is_read = True
        self.save()

    def __str__(self):
        if self.private_room:
            return f'{self.private_room.user2}님! {self.sender}님이 1:1 메시지를 보냈어요💌'
        if self.chat_room:
            return f'{self.sender}님이 {self.chat_room.room_name}에서 메시지를 보냈어요💌'


class Reports(models.Model):
    chat = models.ForeignKey(Chats, on_delete=models.CASCADE)
    reporter = models.ForeignKey(User, related_name='reports_made', on_delete=models.CASCADE)
    reported = models.ForeignKey(User, related_name='reports_received', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.reporter}님이 {self.reported}님을 신고함 사유: {self.content}'


class Notification(models.Model):
    notification_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 유저 FK
    chat = models.ForeignKey(Chats, on_delete=models.CASCADE)  # Chat FK
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}님이게 온 새로운 메세지:{self.message}'
    
class Message(models.Model):
    room = models.ForeignKey(PrivateChatRoom, on_delete=models.CASCADE, related_name="messages")
    sender_email = models.EmailField()
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
