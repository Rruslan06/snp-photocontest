from rest_framework import serializers
from models_app.models import Photo, Comment

class PhotoSerializer(serializers.ModelSerializer):

    author_name = serializers.CharField(source='author.username', read_only=True)

    
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Photo
        
        fields = ['id', 'name', 'description', 'photo', 'date', 'status', 'author_name', 'author',]

        read_only_fields = ['status']


class CommentSerializer(serializers.ModelSerializer):

    author_name = serializers.CharField(source='author.username', read_only=True)

    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment

        fields = ['id', 'text', 'date', 'author_name', 'parent', 'author', 'photo']

        read_only_fields = ['photo']