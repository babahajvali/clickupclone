from urllib.parse import parse_qs

import jwt
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections


class QueryStringJWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        close_old_connections()

        scope["user"] = AnonymousUser()
        scope["user_id"] = None

        token = self._get_token(scope=scope)
        if token:
            user_id = await self._decode_token(token=token)
            scope["user_id"] = user_id

        return await super().__call__(scope, receive, send)

    @staticmethod
    def _get_token(scope) -> str | None:
        query_string = scope.get("query_string", b"").decode()
        token = parse_qs(query_string).get("token", [None])[0]
        if token:
            return token

        for header_name, header_value in scope.get("headers", []):
            if header_name == b"authorization":
                auth_header = header_value.decode()
                if auth_header.startswith("Bearer "):
                    return auth_header.split(" ", 1)[1]

        return None

    @database_sync_to_async
    def _decode_token(self, token: str) -> str | None:
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
            )
            return payload.get("user_id")
        except jwt.PyJWTError:
            return None
