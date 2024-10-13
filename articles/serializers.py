from requests import request
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from articles.models import (
    Articles, 
    ArticleImages, 
    Comments,
)
from users.models import Evaluations
from users.serializers import (
    UserProfileSerializer
)
from django.contrib.auth import get_user_model

User = get_user_model()

class ArticleImageSerializer(serializers.ModelSerializer):
    class Meta :
        model=ArticleImages
        fields='__all__'
        read_only_fields = ['article',]


class CommentSerializer(serializers.ModelSerializer):
    class Meta :
        model=Comments
        fields=['content']
        read_only_fields = ['article', 'user',]


class ArticleSerializer(serializers.ModelSerializer):
    article_images = ArticleImageSerializer(many=True)

    class Meta :
        model=Articles
        fields= ['title', 'content', 'article_score', 'article_images', 'reviewer', 'reviewee']
    
    def create(self, validated_data):
        article = Articles.objects.create(**validated_data)
        img_files = self.context['request'].FILES
        if img_files:
            for img_file in img_files.getlist('img'):
                    ArticleImages.objects.create(article=article, img=img_file)
        req_data = self.context['request'].data
        target_evaluation_data = {
            'kindness': int(req_data.get('kindness', 0)),
            'teamwork': int(req_data.get('teamwork', 0)),
            'communication': int(req_data.get('communication', 0)),
            'mental_strength': int(req_data.get('mental_strength', 0)),
            'punctuality': int(req_data.get('punctuality', 0)),
            'positivity': int(req_data.get('positivity', 0)),
            'mvp': int(req_data.get('mvp', 0)),
            'mechanical_skill': int(req_data.get('mechanical_skill', 0)),
            'operation': int(req_data.get('operation', 0)),
            'negativity': int(req_data.get('negativity', 0)),
            'profanity': int(req_data.get('profanity', 0)),
            'afk': int(req_data.get('afk', 0)),
            'cheating': int(req_data.get('cheating', 0)),
            'verbal_abuse': int(req_data.get('verbal_abuse', 0)),
            }
        if Evaluations.objects.filter(user_id=article.reviewee).exists():
            Evaluations.objects.update(**target_evaluation_data)
        else:
            Evaluations.objects.create(user=article.reviewee, **target_evaluation_data)
        return article


class ArticleReadSerializer(serializers.ModelSerializer):
    # profile = 
    comments = CommentSerializer(many=True, read_only=True)
    class Meta :
        model=Articles
        fields= ['title', 'content', 'article_score', 'created_at', 'reviewer', 'reviewee', 'comments']