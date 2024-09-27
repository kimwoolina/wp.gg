from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass


class Platform(models.Model):
    platform_name = models.CharField(max_length=50)


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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    kindness = models.IntegerField(default=0) # 상냥함
    teamwork = models.IntegerField(default=0) # 팀워크
    communication = models.IntegerField(default=0) # 소통
    mental_strength = models.IntegerField(default=0) #멘탈
    punctualiity= models.IntegerField(default=0) #시간약속
    positivity = models.IntegerField(default=0) #긍정적
    mvp = models.IntegerField(default=0) 
    mechanical_skill = models.IntegerField(default=0) #피지컬
    operation = models.IntegerField(default=0) #운영능력
    negativity = models.IntegerField(default=0) #부정적태도
    profanity = models.IntegerField(default=0) #욕설
    afk = models.IntegerField(default=0) #탈주/자리비움
    cheating = models.IntegerField(default=0) #핵사용
    verbal_abuse= models.IntegerField(default=0) #언어폭력
    