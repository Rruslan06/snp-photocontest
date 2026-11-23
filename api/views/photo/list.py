from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from service_objects.services import ServiceOutcome

from api.services.photo.list import PhotoListService
from api.serializers.photo.list import PhotoListSerializer
from utils.pagination import CustomPagination
from api.docs.photo.photo import LIST_PHOTO




class PhotoListAPIView(APIView):


    @extend_schema(**LIST_PHOTO)
    def get(self, request, *args, **kwargs):
        
        #Забираем параметры из URL 
        params = request.query_params.dict()
               
        
        outcome = ServiceOutcome(PhotoListService, params)
        
        return Response(
            {
                "pagination": CustomPagination(
                    outcome.result,
                    current_page=outcome.service.cleaned_data["page"],
                    per_page=outcome.service.cleaned_data["per_page"],
                ).to_json(),
                "results": PhotoListSerializer(outcome.result, many=True, context={'request': request}).data,
            },
            status=status.HTTP_200_OK,
        )
