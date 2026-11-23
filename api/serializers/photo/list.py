from rest_framework import serializers
from models_app.models import Photo, Comment

class PhotoListSerializer(serializers.ModelSerializer):

    author_name = serializers.CharField(source='author.username', read_only=True)

    likes_count = serializers.IntegerField(read_only=True, default=0)

    comment_count = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = Photo
        
        fields = ['id', 'name', 'description', 'photo', 'date', 'author_name', 'likes_count', 'comment_count']


