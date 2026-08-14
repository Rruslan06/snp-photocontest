from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from models_app.models import Photo, Comment, Vote
from api.serializers import PhotoSerializer, CommentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser



class CommentApiView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer


    def get_queryset(self):
        photo_id = self.kwargs.get('photo_id')
        return Comment.objects.filter(photo_id=photo_id, parent=None)
    
    def perform_create(self, serializer):
        
        photo_id = self.kwargs.get('photo_id')
        serializer.save(photo_id=photo_id)
