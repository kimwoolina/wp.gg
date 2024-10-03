from rest_framework import serializers
from articles.models import (
    Articles, 
    ArticleImages, 
)

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
    class Meta :
        model=Articles
        fields='__all__'
        read_only_fields = ['reviewer',]
    
    def create(self, validated_data):
        return Articles.objects.create(**validated_data)
    
    # def update(self, instance, validated_data):
    #     pass
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        article_images = instance.article_images.all()
        article_image_serializer = ArticleImageSerializer(article_images, many=True)
        ret['article_images'] = article_image_serializer.data
        return ret


class ArticleDetailSerializer(ArticleSerializer):
    pass