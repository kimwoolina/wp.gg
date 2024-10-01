# serializers.py
from rest_framework import serializers
from .models import User, Evaluations, Positions
from articles.models import Articles 


class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluations
        fields = '__all__'


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
        fields = ['username', 'riot_username', 'riot_tag', 'riot_tier', 'positions', 'evaluations', 'articles']
