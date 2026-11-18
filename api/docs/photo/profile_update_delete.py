from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter

from utils.docs_typed_dict import DocsDict
from models_app.models.photo import Photo_Status

from api.serializers.photo.profile import ProfilePhotoSerializer
from api.serializers.photo.update import PhotoUpdateSerializer


PROFILE_PHOTOS: DocsDict = {
    "tags": ["profile"],
    "description": "Получить список фотографий текущего пользователя",
    "parameters": [
        OpenApiParameter(
            name="status_filter",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            required=False,
            description="Фильтр по статусу (MOD, APR, REG)",
            enum=[s[0] for s in Photo_Status.choices]
        ),
        OpenApiParameter(name="page", type=OpenApiTypes.INT, location=OpenApiParameter.QUERY),
        OpenApiParameter(name="per_page", type=OpenApiTypes.INT, location=OpenApiParameter.QUERY),
    ],
    "responses": {200: ProfilePhotoSerializer(many=True)}, # Тут профиль-сериализатор заменил
}

UPDATE_PHOTO: DocsDict = {
    "tags": ["photo"],
    "description": "Частичное изменение своей фотографии",
    "request": PhotoUpdateSerializer, # Сериализатор заменил
    "responses": {200: PhotoUpdateSerializer},
}

DELETE_PHOTO: DocsDict = {
    "tags": ["photo"],
    "description": "Удаление своей фотографии",
    "responses": {204: None},
}


RESTORE_PHOTO: DocsDict = {
    "tags": ["photo"],
    "description": "Отменить удаление фотографии (восстановить)",
    "responses": {200: None}, # Мы просто возвращаем сообщение
}