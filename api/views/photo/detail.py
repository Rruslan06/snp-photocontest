from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from drf_spectacular.utils import extend_schema
from service_objects.services import ServiceOutcome

# Сервисы
from api.services.photo.show import PhotoShowService
from api.services.photo.update import PhotoUpdateService
from api.services.photo.delete import PhotoDeleteService

# Сериализаторы и Доки
from api.serializers.photo.show import PhotoSerializer
from api.serializers.photo.update import PhotoUpdateSerializer
from api.docs.photo.photo import SHOW_PHOTO
from api.docs.photo.profile_update_delete import UPDATE_PHOTO, DELETE_PHOTO

class PhotoDetailAPIView(APIView):
    """
    Единый эндпоинт для работы с одной фотографией: GET, PATCH, DELETE.
    """
    
    parser_classes = [MultiPartParser, FormParser]

    @extend_schema(**SHOW_PHOTO)
    def get(self, request, photo_id, *args, **kwargs):
        """Просмотр одной фотографии"""
        user = request.user if request.user.is_authenticated else None
        outcome = ServiceOutcome(PhotoShowService, {'photo_id': photo_id, 'user': user})
        serializer = PhotoSerializer(outcome.result, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)



    @extend_schema(**UPDATE_PHOTO)
    def patch(self, request, photo_id, *args, **kwargs):
        """Частичное изменение фотографии"""


        data = request.data.dict() if hasattr(request.data, 'dict') else request.data.copy()
        data['photo_id'] = photo_id
        data['user'] = request.user
        
        outcome = ServiceOutcome(PhotoUpdateService, data, request.FILES)
        serializer = PhotoUpdateSerializer(outcome.result, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)



    @extend_schema(**DELETE_PHOTO)
    def delete(self, request, photo_id, *args, **kwargs):
        """Удаление фотографии"""

        outcome = ServiceOutcome(PhotoDeleteService, {'photo_id': photo_id, 'user': request.user})
        return Response(outcome.result, status=status.HTTP_204_NO_CONTENT)