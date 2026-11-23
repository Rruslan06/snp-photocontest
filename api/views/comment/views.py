from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from models_app.models import Photo, Comment, Vote
from api.serializers.comment.comment import CommentSerializer
from api.serializers.photo.show import PhotoSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class CommentApiView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer


    def get_queryset(self):
        photo_id = self.kwargs.get('photo_id')
        return Comment.objects.filter(photo_id=photo_id, parent=None)
    
    def perform_create(self, serializer):
        
        photo_id = self.kwargs.get('photo_id')

        comment = serializer.save(photo_id=photo_id)

    # Получаем фотку, чтобы узнать автора
        photo = comment.photo
        comments_count = photo.comments.count()
        
        if self.request.user.id != photo.author.id:
            message = f"Пользователь {self.request.user.username} оставил комментарий к вашему фото '{photo.name}'. Всего комментариев: {comments_count}"
            
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"user_{photo.author.id}",
                {"type": "send_notification", "message": message}
            )
