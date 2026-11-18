from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from service_objects.services import ServiceOutcome

from api.serializers.comment.comment import CommentSerializer
from api.services.comment.update import CommentUpdateService
from api.services.comment.delete import CommentDeleteService
from api.docs.comment.comment import UPDATE_COMMENT, DELETE_COMMENT

class CommentDetailAPIView(APIView):
    """
    Единый эндпоинт для действий с конкретным комментарием: PATCH (изменение) и DELETE (удаление).
    """

    @extend_schema(**UPDATE_COMMENT)
    def patch(self, request, comment_id, *args, **kwargs):
        data = request.data.dict() if hasattr(request.data, 'dict') else request.data.copy()
        data['comment_id'] = comment_id
        data['user'] = request.user
        
        outcome = ServiceOutcome(CommentUpdateService, data)
        serializer = CommentSerializer(outcome.result, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)



    @extend_schema(**DELETE_COMMENT)
    def delete(self, request, comment_id, *args, **kwargs):
        outcome = ServiceOutcome(CommentDeleteService, {'comment_id': comment_id, 'user': request.user})
        return Response(outcome.result, status=status.HTTP_204_NO_CONTENT)