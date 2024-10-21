from django.db import models
from users.models import User


class Parties(models.Model):
    # 성별 선택
    GENDER_CHOICES = [
        # M은 저장되는 값, Male은 사용자에게 표시되는 값
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    # 나이 선택
    AGE_CHOICES = [
        # 20은 저장되는 값, 청소년은 사용자에게 표시되는 값
        ("10", "청소년"),
        ('20', '청년'),
        ('30', '중년'),
        ('40', '중장년'),
    ]
    
    # 랭크 선택
    RANK_CHOICES = [
        # 0은 저장되는 값, Unranked는 사용자에게 표시되는 값
        ("0", "Unranked"),
        ("1", "Iron"),
        ('2', 'Bronze'),
        ('3', 'Silver'),
        ('4', 'Gold'),
        ('5', 'Platinum'),
        ('6', 'Amarald'),
        ('7', 'Diamond'),
        ('8', 'Master'),
        ('9', 'Grand Master'),
        ("10", "Challenger"),
    ]
    
    # 서버 선택
    SERVER_CHOICES = [
        # KR은 저장되는 값, KR1는 사용자에게 표시되는 값
        ("KR", "KR1"),
        ("LAN", "LA1"),
        ("LAS", "LA2"),
        ("RU", "RU1"),
        ("NA", "NA1"),
        ("BR", "BR1"),
        ("OCE", "OC1"),
        ("EUNE", "EUN1"),
        ("EUW", "EUW1"),
        ("JP", "JP1"),
        ("TR", "TR1"),
        ("SG", "SG2"),
        ("TH", "TH2"),
        ("PH", "PH2"),
        ("ME", "ME1"),
    ]
    
    # 언어 선택
    LANGUAGE_CHOICE = [
        # KR은 저장되는 값, 한국어는 사용자에게 표시되는 값
        # 언어는 상의 후에 추가(아는게 이거밖에 없음ㅠㅠ)
        ("KR", "한국어"),
        ("EN", "ENGLISH"),
        ("JP", "日本語"),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rank = models.CharField(max_length=2, choices=RANK_CHOICES)
    server = models.CharField(max_length=4, choices=SERVER_CHOICES)
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICE)
    age = models.CharField(max_length=2, choices=AGE_CHOICES)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_rank = models.BooleanField(default=False)
    
    # Party1
    top1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="party_top1", null=True)
    jungle1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="party_jungle1", null=True)
    mid1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="party_mid1", null=True)
    support1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="party_support1", null=True)
    adc1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="party_adc1", null=True)
    
    # Party2
    top2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="party_top2", null=True)
    jungle2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="party_jungle2", null=True)
    mid2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="party_mid2", null=True)
    support2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="party_support2", null=True)
    adc2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="party_adc2", null=True)
