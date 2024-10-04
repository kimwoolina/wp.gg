from requests import request
from rest_framework import serializers
from articles.models import (
    Articles, 
    ArticleImages, 
)
from users.models import Evaluations
from users.serializers import EvaluationSerializer

class ArticleImageSerializer(serializers.ModelSerializer):
    class Meta :
        model=ArticleImages
        fields='__all__'
        read_only_fields = ['article',]

    def create(self, validated_data):
        return Articles.objects.create(**validated_data)
    
    # def update(self, instance, validated_data):
    #     pass


class CommentSerializer(serializers.ModelSerializer):
    pass


class ArticleSerializer(serializers.ModelSerializer):
    article_images = ArticleImageSerializer(many=True, read_only=True)

    class Meta :
        model=Articles
        fields= ['title', 'content', 'article_score', 'reviewee', 'article_images']
        read_only_fields = ['reviewer',]
    
    def create(self, validated_data):
        article = Articles.objects.create(**validated_data)
        img_files = self.context['request'].FILES
        for img_file in img_files.getlist('img'):
            ArticleImages.objects.create(article=article, img=img_file)
        return article
    
    # def update(self, instance, validated_data):
    #     pass


class ArticleDetailSerializer(ArticleSerializer):                    
    pass