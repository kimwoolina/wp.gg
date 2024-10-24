from rest_framework import serializers
from users.models import User, Evaluations, Positions
from articles.models import Articles 
import logging

# 로깅 객체 생성
logger = logging.getLogger('django')

class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluations
        read_only_fields = ['user',]
        exclude = ['created_at', 'updated_at',]

    def create(self, validated_data):
        try:
                evaluation = Evaluations.objects.create(**validated_data)
                return evaluation
        except Exception as e:
            logger.error(f"Failed to create evaluation: {e}")
            raise serializers.ValidationError("Failed to create evaluation.")

    def update(self, instance, validated_data):
        for field in validated_data:
            setattr(instance, field, getattr(instance, field, 0) + validated_data[field])
        instance.save()
        return instance


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Positions
        fields = ['position_name']

        
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articles
        fields = ['id', 'title', 'article_score', 'created_at', 'reviewer'] 


class UserSerializer(serializers.ModelSerializer):
    evaluations = EvaluationSerializer(read_only=True)
    positions = PositionSerializer(many=True, read_only=True)
    articles = ArticleSerializer(many=True, read_only=True) 

    class Meta:
        model = User
        fields = ['username', 'profile_image', 'riot_username', 'riot_tag', 'riot_tier', 'positions', 'score', 'evaluations', 'articles']


class UserRankingSerializer(serializers.ModelSerializer):
    evaluations = EvaluationSerializer(read_only=True)
    positions = PositionSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['username', 'riot_username', 'riot_tag', 'riot_tier', 'positions', 'score', 'evaluations',]
