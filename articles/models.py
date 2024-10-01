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
        )
    reviewee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviewees"
        )
    like_users = models.ManyToManyField(
        User, symmetrical=False, related_name="like_article", through="Likes"
        )
    comment = models.ManyToManyField(
        User, symmetrical=False, related_name="article_comments", through="Comments"
        )


class Article_images(models.Model):
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
    