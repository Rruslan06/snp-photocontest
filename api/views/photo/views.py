from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from models_app.models import Photo, Comment, Vote
from api.serializers import PhotoSerializer, CommentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from service_objects.services import ServiceOutcome
from rest_framework import status
from drf_spectacular.utils import extend_schema 


class PhotoListAPIView(APIView):

    parser_classes = [MultiPartParser, FormParser]

    @extend_schema(responses=PhotoSerializer(many=True))
    def get(self, request, *args, **kwargs):
        """Обрабатываем GET запрос (Отдаем список фото)"""
        
        photos = Photo.objects.filter(status='APR')
        
        serializer = PhotoSerializer(photos, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)


    @extend_schema(request=PhotoSerializer, responses=PhotoSerializer)
    def post(self, request, *args, **kwargs):
        """Обрабатываем POST запрос (Создаем фото)"""
        
        serializer = PhotoSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
           
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#Здесь можно не передавать get для поиска по pk, он делает сам
#Если хочется искать не по <int:pk>/<str:pk> а по какому-нибудь slug, надо поменять параметр lookup_field(пример ниже закомментирован)
class PhotoDetailAPIView(generics.RetrieveAPIView):

    queryset = Photo.objects.all()
    #lookup_field = 'slug'
    serializer_class = PhotoSerializer


class ShowPhotoView(APIView):
    pass
#     def get(self, request, *args, **kwargs) -> Response:
#         outcome = ServiceOutcome(S, {"id": kwargs["id"]})


#     # class RetrieveUpdateRegionView(APIView):
#     # @extend_schema(**SHOW_REGION)
#     # def get(self, request, *args, **kwargs) -> Response:
#     #     outcome = ServiceOutcome(RegionShowService, {"id": kwargs["id"]})
#     #     return Response(
#     #         RegionShowSerializer(outcome.result).data,
#     #         status=status.HTTP_200_OK,
#     #    )