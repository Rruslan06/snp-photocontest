from rest_framework import serializers

class VoteResponseSerializer(serializers.Serializer):
    
    liked = serializers.BooleanField()
    likes_count = serializers.IntegerField()