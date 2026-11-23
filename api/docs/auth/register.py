from utils.docs_typed_dict import DocsDict
from api.serializers.auth.register import RegisterRequestSerializer, RegisterResponseSerializer

REGISTER_USER: DocsDict = {
    "tags": ["auth"],
    "description": "Регистрация нового пользователя и выдача JWT токена",
    "request": RegisterRequestSerializer,
    "responses": {201: RegisterResponseSerializer},
}