from django.db import models
from users.models import User, Chats

class Reports(models.Model):
    chat = models.ForeignKey(Chats, on_delete=models.CASCADE) #FK
    reporter =  models.ForeignKey(User, on_delete=models.CASCADE) # 신고하는 사람(FK)
    reported = models.ForeignKey(User, on_delete=models.CASCADE) # 신고당하는 사람 (FK)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)