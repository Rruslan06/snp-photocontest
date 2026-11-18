from rest_framework import serializers
from models_app.models import Photo


class PhotoSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    likes_count = serializers.IntegerField(read_only=True)
    has_voted = serializers.BooleanField(read_only=True)

    class Meta:
        model = Photo
        fields = [
            'id', 'name', 'description', 'photo', 'date',
            'status', 'author_name', 'author', 'likes_count', 'has_voted'
        ]
        read_only_fields = ['status']