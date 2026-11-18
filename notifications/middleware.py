from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from models_app.models import User


@database_sync_to_async
def get_user(token_key):
    try:
        access_token = AccessToken(token_key)

        return User.objects.get(id=access_token['user_id'])
    
    except Exception:
        return AnonymousUser()

class TokenAuthMiddleware:
    """Аутентификация для WebSockets через JWT токен в URL"""
    def __init__(self, inner):
        self.inner = inner  #Как я понял, это наш консьюмер


    async def __call__(self, scope, receive, send):
        # Токен из ссылки
        query_string = parse_qs(scope['query_string'].decode())
        token = query_string.get('token')
        
        if token:
            scope['user'] = await get_user(token[0])
        else:
            scope['user'] = AnonymousUser()
            
        return await self.inner(scope, receive, send)