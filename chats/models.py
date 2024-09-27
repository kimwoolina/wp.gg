from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Chats(models.Model):
    sender = models.ForeignKey(User, related_name='sent_chats', on_delete=models.CASCADE)  
    receiver = models.ForeignKey(User, related_name='received_chats', on_delete=models.CASCADE)  
    content = models.TextField()  
    is_read = models.BooleanField(default=False)  
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True) 

    def mark_as_read(self):
        """메시지 읽음 표시"""
        self.is_read = True  
        self.save()

    def __str__(self):
        return f'{self.receiver}님! {self.sender}님이 메시지를 보냈어요💌'


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    chat = models.ForeignKey(Chats, null=True, blank=True, related_name='notifications', on_delete=models.CASCADE) 
    is_read = models.BooleanField(default=False)  
    created_at = models.DateTimeField(auto_now_add=True)  

    def mark_as_read(self):
        """알림 읽음 표시 후 해당 채팅도 읽음 상태로 업데이트"""
        self.is_read = True
        self.save()

        if self.chat:
            self.chat.mark_as_read() 

    def __str__(self):
        if self.chat:
            return f'{self.chat.receiver}님, {self.chat.sender}님에게 새 메시지가 왔습니다!'
        return f'{self.user}님 새로운 알림을 확인해보세요📮'


class Reports(models.Model):
    chat = models.ForeignKey(Chats, on_delete=models.CASCADE) #FK
    reporter =  models.ForeignKey(User, on_delete=models.CASCADE) # 신고하는 사람(FK)
    reported = models.ForeignKey(User, on_delete=models.CASCADE) # 신고당하는 사람 (FK)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    