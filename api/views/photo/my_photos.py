from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from service_objects.services import ServiceOutcome

from api.serializers.photo.list import PhotoListSerializer
from api.serializers.photo.profile import ProfilePhotoSerializer
from utils.pagination import CustomPagination
from models_app.models.photo import Photo_Status
from api.services.photo.my_photos import ProfilePhotoListService

from api.docs.photo.profile_update_delete import PROFILE_PHOTOS

from rest_framework.permissions import IsAuthenticated

class ProfilePhotoListAPIView(APIView):

    permission_classes = [IsAuthenticated]
    
    @extend_schema(**PROFILE_PHOTOS)
    def get(self, request, *args, **kwargs):
       
        params = request.query_params.dict()
        params['user'] = request.user 
        
        
        outcome = ServiceOutcome(ProfilePhotoListService, params)
        
        
        return Response(
            {
                "pagination": CustomPagination(
                    outcome.result,
                    current_page=outcome.service.cleaned_data.get("page") or 1,
                    per_page=outcome.service.cleaned_data.get("per_page") or 8,
                ).to_json(),
                "results": ProfilePhotoSerializer(outcome.result, many=True, context={'request': request}).data,
            },
            status=status.HTTP_200_OK,
        )