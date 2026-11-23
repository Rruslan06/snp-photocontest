from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter

from utils.docs_typed_dict import DocsDict
from api.services.photo.list import SortField, SortDirection
from api.serializers.photo.list import PhotoListSerializer
from api.serializers.photo.show import PhotoSerializer
from api.serializers.photo.create import PhotoCreateSerializer  


LIST_PHOTO: DocsDict = {
    "tags": ["photo"],
    "description": "List Photos",
    "parameters": [
        OpenApiParameter(
            name="search_query",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            required=False,
            description="Поиск по автору/названию/описанию",
        ),

        OpenApiParameter(
            name="sort_field",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            required=False,
            description="Тип для сортировки",
            enum=SortField.values
        ),

        OpenApiParameter(
            name="sort_direction",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            required=False,
            description="направление сортировки",
            enum=SortDirection.values
        ),


        OpenApiParameter(
            name="page",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            required=False,
            description="Page number",
            default=1,
        ),
        OpenApiParameter(
            name="per_page",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            required=False,
            description="Objects per page",
            default=10,
        ),
    ],
    "responses": {200: PhotoListSerializer(many=True)},
}


SHOW_PHOTO: DocsDict = {
    "tags": ["photo"],
    "description": "Просмотр одной фотографии",
    "responses": {200: PhotoSerializer},
}

CREATE_PHOTO: DocsDict = {
    "tags": ["photo"],
    "description": "Создание новой фотографии",
    "request": PhotoCreateSerializer,
    "responses": {201: PhotoCreateSerializer},
}