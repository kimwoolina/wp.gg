from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

# User = get_user_model()

class Positions(models.Model):
    position_name = models.CharField(max_length=7)

class User(AbstractUser):
    username = models.CharField(max_length=15, unique=True) 
    riot_username = models.CharField(max_length=15, null=True, blank=True)  # 리그 오브 레전드 유저명
    riot_tag = models.CharField(max_length=15, null=True, blank=True)  # 리그 오브 레전드 서버명
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
    platforms = models.ManyToManyField('Platform', through='UserPlatform', related_name='users')
    is_notification_sound_on = models.BooleanField(default=True)  # 알람 소리 
    is_notification_message_on = models.BooleanField(default=True)  # 알람 메시지

    def __str__(self):
        return self.username
    
    class Meta:
        ordering = ['-date_joined']  # 가입일 기준 내림차순 정렬


class Platform(models.Model):
    platform_name = models.CharField(max_length=50)


# User-Platform 중계테이블
class UserPlatform(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) #FK
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE) #FK
    joined_date  = models.DateField(auto_now_add=True)
    
    class Meta:
        # user와 platform의 조합이 고유해야 함
        constraints = [
            models.UniqueConstraint(fields=['user', 'platform'], name='unique_user_platform')
        ] 
    
    def __str__(self):
        return f"{self.user.username} - {self.platform.name}"


class Evaluations(models.Model):
    #evaluation_id = models.CharField(max_length=20) #메모리 관리를 위한 고유 ID (ex: EV0001) # 뷰에서 로직구현 필요
    #user = models.ForeignKey(User, on_delete=models.CASCADE) #FK
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # 1:1 관계
    kindness = models.IntegerField(default=0) # 상냥함
    teamwork = models.IntegerField(default=0) # 팀워크
    communication = models.IntegerField(default=0) # 소통
    mental_strength = models.IntegerField(default=0) #멘탈
    punctuality= models.IntegerField(default=0) #시간약속
    positivity = models.IntegerField(default=0) #긍정적
    mvp = models.IntegerField(default=0) 
    mechanical_skill = models.IntegerField(default=0) #피지컬
    operation = models.IntegerField(default=0) #운영능력
    negativity = models.IntegerField(default=0) #부정적태도
    profanity = models.IntegerField(default=0) #욕설
    afk = models.IntegerField(default=0) #탈주/자리비움
    cheating = models.IntegerField(default=0) #핵사용
    verbal_abuse= models.IntegerField(default=0) #언어폭력
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

from .managers import DiscordUserOAuth2Manager

class DiscordUser(models.Model):
    objects = DiscordUserOAuth2Manager()
    id = models.BigIntegerField(primary_key=True)
    discordTag = models.CharField(max_length=37)
    avatar = models.CharField(max_length=100)
    publicFlags = models.IntegerField()
    flags = models.IntegerField()
    locale = models.CharField(max_length=100)
    mfaEnabled = models.BooleanField()
    last_login = models.DateTimeField()
    
    def is_authenticated(self, request):
        return True