from rest_framework import serializers
from requests import request
from rest_framework.response import Response
from rest_framework import status
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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'riot_username', 'riot_tag', 'profile_image']


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
    reviewer = UserSerializer()  # reviewer의 프로필 정보를 UserSerializer로 직렬화
    reviewee = UserSerializer()  # reviewee의 프로필 정보를 UserSerializer로 직렬화
    article_images = ArticleImageSerializer(many=True)  # 글에 포함된 이미지를 직렬화
    
    class Meta:
        model = Articles
        fields = ['id', 'title', 'content', 'article_score', 'article_images', 'reviewer', 'reviewee', 'created_at', 'updated_at']

    def update_user_score(self, reviewee):
        # reviewee가 평가받은 모든 article들의 평균 점수를 계산
        reviews = reviewee.reviewees.all()
        if reviews.exists():
            reviewee.score = reviews.aggregate(Avg('article_score'))['article_score__avg']
        else:
            reviewee.score = 0.0
        reviewee.save()
        
    def create(self, validated_data):
        article = Articles.objects.create(**validated_data)
        
        # 이미지 파일 처리
        img_files = self.context['request'].FILES
        if img_files:
            for img_file in img_files.getlist('img'):
                ArticleImages.objects.create(article=article, img=img_file)

        # 평가 데이터 처리
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

        # 평가가 있으면 업데이트, 없으면 생성
        if Evaluations.objects.filter(user_id=article.reviewee).exists():
            Evaluations.objects.filter(user=article.reviewee).update(**target_evaluation_data)
        else:
            Evaluations.objects.create(user=article.reviewee, **target_evaluation_data)

        # 리뷰어의 점수 업데이트
        self.update_user_score(article.reviewee)

        return article

    
    
    
    def update(self, instance, validated_data):
        article = super().update(instance, validated_data)
        article.update_user_score()  # 아티클이 업데이트될 때 점수 업데이트
        return article


class ArticleReadSerializer(serializers.ModelSerializer):
    # profile = 
    comments = CommentSerializer(many=True, read_only=True)
    class Meta :
        model=Articles
        fields= ['title', 'content', 'article_score', 'created_at', 'reviewer', 'reviewee', 'comments']