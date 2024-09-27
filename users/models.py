from django.db import models
from django.contrib.auth.models import AbstractUser

class Positions(models.Model):
    position_name = models.CharField(max_length=7)

class User(AbstractUser):
    username = models.CharField(max_length=15, unique=True) 
    riot_username = models.CharField(max_length=15, unique=True)  # 리그 오브 레전드 유저명
    riot_tag = models.CharField(max_length=15)  # 리그 오브 레전드 서버명
    discord_username = models.CharField(max_length=15, null=True, blank=True)  # 디스코드 유저명
    discord_tag = models.CharField(max_length=15, null=True, blank=True)  # 디스코드 태그명
    email = models.EmailField(unique=True)  
    date_joined = models.DateField(auto_now_add=True) 
    is_active = models.BooleanField(default=True)  
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    credit_info = models.PositiveIntegerField(null=True, blank=True)  # 충전 금액
    introduction = models.TextField(null=True, blank=True)
    score = models.FloatField(default=0.0)
    is_notified = models.BooleanField(default=False)
    is_blacklist = models.BooleanField(default=False)
    riot_tier = models.CharField(max_length=15, null=True, blank=True)  # 리그 오브 레전드 티어
    positions = models.ManyToManyField(Positions, blank=True, related_name="user")


    def __str__(self):
        return self.username
    
    class Meta:
        ordering = ['-date_joined']  # 가입일 기준 내림차순 정렬

