from django.shortcuts import render
from rest_framework import generics
from models_app.models.photo import Photo
from .serializers import PhotoSerializer

from rest_framework.parsers import MultiPartParser, FormParser


# Create your views here.

class PhotoListAPIView(generics.ListCreateAPIView):
    
    queryset = Photo.objects.filter(status='APR') 
    
    serializer_class = PhotoSerializer

                    # Выбирается нужный класс расшифровки для данных из запроса
                    # Заголовка content-type и потом данные уходят в request.data 
    parser_classes = [MultiPartParser, FormParser]



#Здесь можно не передавать get для поиска по pk, он делает сам
#Если хочется искать не по <int:pk>/<str:pk> а по какому-нибудь slug, надо поменять параметр lookup_field(пример ниже закомментирован)
class PhotoDetailAPIView(generics.RetrieveAPIView):

    queryset = Photo.objects.all()
    #lookup_field = 'slug'
    serializer_class = PhotoSerializer