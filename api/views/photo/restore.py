from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from service_objects.services import ServiceOutcome

from api.services.photo.restore import PhotoRestoreService

from api.docs.photo.profile_update_delete import RESTORE_PHOTO 

class PhotoRestoreAPIView(APIView):

    @extend_schema(**RESTORE_PHOTO)
    def post(self, request, photo_id, *args, **kwargs):
        
        outcome = ServiceOutcome(PhotoRestoreService, {'photo_id': photo_id, 'user': request.user})
        return Response(outcome.result, status=status.HTTP_200_OK)