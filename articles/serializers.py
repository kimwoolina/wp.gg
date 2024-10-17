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
from django.db.models import Avg
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'riot_username', 'riot_tag', 'profile_image']


class CommentSerializer(serializers.ModelSerializer):
    # class Meta :
    #     model=Comments
    #     fields=['content']
    #     read_only_fields = ['article', 'user',]
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comments
        fields = ['id', 'user', 'content', 'created_at', 'updated_at', 'parent_comment']
        
    def create(self, validated_data):
        # 부모 댓글이 없을 때 None 값 허용
        parent_comment = validated_data.get('parent_comment', None)
        return Comments.objects.create(**validated_data)

class ArticleImageSerializer(serializers.ModelSerializer):
    class Meta :
        model=ArticleImages
        fields='__all__'
        read_only_fields = ['article',]


class ArticleDetailSerializer(serializers.ModelSerializer):
    reviewer = UserSerializer(read_only=True)
    reviewee = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    article_images = ArticleImageSerializer(many=True, read_only=True)

    class Meta:
        model = Articles
        fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'reviewer', 'reviewee', 'article_images', 'comments']


class ArticleListSerializer(serializers.ModelSerializer):
    reviewer = UserSerializer()  # reviewer의 프로필 정보를 UserSerializer로 직렬화
    reviewee = UserSerializer()  # reviewee의 프로필 정보를 UserSerializer로 직렬화
    article_images = ArticleImageSerializer(many=True, required=False)  # 글에 포함된 이미지를 직렬화
    
    class Meta:
        model = Articles
        fields = ['id', 'title', 'content', 'article_score', 'article_images', 'reviewer', 'reviewee', 'created_at', 'updated_at']


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articles
        fields = '__all__'
        extra_kwargs = {
            'reviewer': {'read_only': True}  
        }

    def update_user_score(self, reviewee):
        """
        reviewee가 평가받은 모든 article들의 평균 점수를 계산하여 업데이트합니다.
        """
        reviews = reviewee.reviewees.all()
        if reviews.exists():
            reviewee.score = reviews.aggregate(Avg('article_score'))['article_score__avg']
        else:
            reviewee.score = 0.0
        reviewee.save()

    def create(self, validated_data):
        """
        새로운 기사를 생성하고 관련 데이터를 처리합니다.
        """
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['reviewer'] = request.user

        # img_files를 validated_data에 추가
        img_files = self.context.get('article_images', [])
        
        article = Articles.objects.create(**validated_data)
        
        # 이미지 파일 처리
        self._handle_image_files(article, img_files)

        # 평가 데이터 처리
        self._handle_evaluation_data(article)

        # 리뷰어의 점수 업데이트
        self.update_user_score(article.reviewee)

        return article

    def _handle_image_files(self, article, img_files):
        """
        이미지 파일을 처리하여 ArticleImages를 생성합니다.
        """
        # img_files가 비어있지 않은 경우에만 처리
        for img_file in img_files:
            ArticleImages.objects.create(article=article, img=img_file)
                
    def _handle_evaluation_data(self, article):
        """
        평가 데이터를 처리하여 Evaluations 객체를 생성 또는 업데이트합니다.
        체크된 항목에 대해 +1씩 추가합니다.
        """
        req_data = self.context['request'].data
        evaluation, created = Evaluations.objects.get_or_create(user=article.reviewee)

        # 각 항목에 대해 체크 여부에 따라 +1 추가
        for field in [
            'kindness', 'teamwork', 'communication', 'mental_strength', 
            'punctuality', 'positivity', 'mvp', 'mechanical_skill', 
            'operation', 'negativity', 'profanity', 'afk', 
            'cheating', 'verbal_abuse'
        ]:
            if req_data.get(field) == '1':  # 체크된 항목일 경우
                setattr(evaluation, field, getattr(evaluation, field, 0) + 1)

        # 업데이트된 평가 데이터를 저장
        evaluation.save()

    def update(self, instance, validated_data):
        article = super().update(instance, validated_data)
        article.update_user_score()  # 아티클이 업데이트될 때 점수 업데이트
        return article