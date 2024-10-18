from rest_framework import serializers
from .models import Parties


class PartiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parties
        fields = [
            "id",
            "user",
            "rank",
            "server",
            "language",
            "age",
            "gender",
            "created_at",
            "is_rank",
            "top1",
            "jungle1",
            "mid1",
            "support1",
            "adc1",
            "top2",
            "jungle2",
            "mid2",
            "support2",
            "adc2",
        ]