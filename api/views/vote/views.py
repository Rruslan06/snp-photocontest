from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from models_app.models import Photo, Comment, Vote
from api.serializers import PhotoSerializer, CommentSerializer, VoteResponseSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from api.services import ToggleVoteService
from rest_framework import status
from drf_spectacular.utils import extend_schema 
from service_objects.services import ServiceOutcome
    


class VoteAPIView(APIView):



    @extend_schema(request=None, responses=VoteResponseSerializer)
    def post(self, request, photo_id, ):

        # result_dict = ToggleVoteService.execute({
        #     'photo_id': photo_id,
        #     'user_id': request.user.id
        # })

        outcome = ServiceOutcome(ToggleVoteService, {"photo_id": photo_id, "user": request.user})

        
        return Response(None, status=status.HTTP_200_OK)