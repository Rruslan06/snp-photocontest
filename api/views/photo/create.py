from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from drf_spectacular.utils import extend_schema
from service_objects.services import ServiceOutcome

from api.services.photo.create import PhotoCreateService
from api.serializers.photo.create import PhotoCreateSerializer
from api.docs.photo.photo import CREATE_PHOTO



class PhotoCreateAPIView(APIView):

    parser_classes = [MultiPartParser, FormParser]


    @extend_schema(**CREATE_PHOTO)
    def post(self, request, *args, **kwargs):
        """Создание фото через PhotoCreateService"""
        
        data = request.data.dict() if hasattr(request.data, 'dict') else request.data.copy()
        data['author'] = request.user # Подкидываем юзера
        
        # Вызываем сервис
        # В data прокидывается только текст, но не картинка, поэтому ругался и добавили параметр для картинки
        service = PhotoCreateService.execute(data, request.FILES)
        
        # Сериализуем результат
        serializer = PhotoCreateSerializer(service.result, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

