from rest_framework import serializers
from .models import User
from rest_framework import serializers
from .models import User, Evaluations, Positions
from articles.models import Articles 


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


class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluations
        read_only_fields = ['user',]
        exclude = ['created_at', 'updated_at',]

    def create(self, validated_data):
        return Evaluations.objects.create(**validated_data)

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
        fields = ['username', 'riot_username', 'riot_tag', 'riot_tier', 'positions', 'evaluations', 'articles']

class UserRankingSerializer(serializers.ModelSerializer):
    evaluations = EvaluationSerializer(read_only=True)
    positions = PositionSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['username', 'riot_username', 'riot_tag', 'riot_tier', 'positions', 'score', 'evaluations',]


# from lib.social_account import discord
# from lib.register.register import register_social_user

# class DiscordAuthSerializer(serializers.Serializer):
#     """Handles serialization of discord related data"""
#     auth_token = serializers.CharField()
#     def validate_auth_token(self, auth_token):
#         user_data =  discord.Discord.validate(auth_token)
#         try:
#             email = user_data['email']
#             provider = 'discord'
#         except:
#             raise serializers.ValidationError(
#                 'The token  is invalid or expired. Please login again.'
#             )
#         return register_social_user(
#             provider=provider, user_id=None, email=email, name=None)