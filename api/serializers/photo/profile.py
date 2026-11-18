from rest_framework import serializers
from models_app.models import Photo

class ProfilePhotoSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Photo
        fields = ['id', 'name', 'photo', 'date', 'status', 'author_name']