from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema
from service_objects.services import ServiceOutcome
from service_objects.errors import InvalidInputsError

from api.services.auth.register import UserRegisterService
from api.serializers.auth.register import RegisterResponseSerializer
from api.docs.auth.register import REGISTER_USER


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(**REGISTER_USER)
    def post(self, request, *args, **kwargs):
        try:
            outcome = ServiceOutcome(UserRegisterService, request.data)
        except InvalidInputsError as e:
            return Response({"errors": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        user = outcome.result
        refresh = RefreshToken.for_user(user)

        serializer = RegisterResponseSerializer({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        })
        return Response(serializer.data, status=status.HTTP_201_CREATED)