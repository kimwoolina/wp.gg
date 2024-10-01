from django.db import models
from django.contrib.auth import get_user_model

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
    