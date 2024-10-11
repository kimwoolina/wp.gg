from rest_framework import serializers
from .models import User
from rest_framework import serializers
from .models import User, Evaluations, Positions
from articles.models import Articles 
from rest_framework import serializers
from .models import User
from rest_framework import serializers
from .validators import validate_email, validate_username_length


class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluations
        exclude = ('created_at', 'updated_at')


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
        fields = ['username', 'email', 'riot_username', 'riot_tag', 'riot_tier', 'positions', 'evaluations', 'articles']


    def validate_email(self, value):
        validate_email(value)
        return value

    def validate_username(self, value):
        validate_username_length(value)
        return value
    

class UserRankingSerializer(serializers.ModelSerializer):
    evaluations = EvaluationSerializer(read_only=True)
    positions = PositionSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['username', 'riot_username', 'riot_tag', 'riot_tier', 'positions', 'score', 'evaluations',]
        

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username', 
            'email', 
            'profile_image', 
            'platforms', 
            'riot_username', 
            'riot_tag', 
            'introduction', 
            'is_notification_sound_on',  # 알람 소리 설정
            'is_notification_message_on'  # 알람 메시지 설정
        ]
