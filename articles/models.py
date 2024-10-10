from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

User = get_user_model()


class Articles(models.Model):
    title = models.CharField(max_length=120)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    article_score = models.IntegerField(default=0)
    reviewer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviewers"
        ) # reviewer == 평가 하는 사람 id
    reviewee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviewees"
        ) # reviewee == 평가 받는 사람 id
    like_users = models.ManyToManyField(
        User, symmetrical=False, related_name="like_article", through="Likes"
        )
    comment = models.ManyToManyField(
        User, symmetrical=False, related_name="article_comments", through="Comments"
        )


# receiver:특정 이벤트 발생 시 실행되는 함수(post_save: db 저장 후 실행 / post_delete: db 제거 후 실행, 
#                                          sender: 어떤 모델에서 신호를 받을지)
# @receiver(post_save, sender=Articles)
# @receiver(post_delete, sender=Articles)
# def update_like_count(sender, instance, **kwargs):
#     #평가 대상 유저
#     user = instance.user
    
#     # 해당 유저에 대한 모든 평가 가져오기
#     reviews = user.reviewees.all()
    
#     # 유저에 대한 평가가 있을 경우 평균 점수 계산, 없으면 0으로 설정
#     if reviews.exist():
#         # articvle_score 필드의 평균값
#         user.score = reviews.aggregate(models.Avg('article_score'))['score__avg']
#         # reviews.aggregate(models.Avg('article_score'))가 딕셔너리 형태로 저장된다고 해서 테스트용 print
#         print(user.score)
#     else:
#         user.score = 0
#     user.save()
    
    
class ArticleImages(models.Model):
    article = models.ForeignKey(
        Articles, on_delete=models.CASCADE, related_name="article_images"
        )
    created_at = models.DateTimeField(auto_now_add=True)
    img = models.ImageField(upload_to="%Y/%m/%d", blank=True, null=True)
    
    
class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Articles, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Articles, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    