import jwt
from django.conf import settings
from django.http import JsonResponse
import json


class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.path.startswith('/graphql'):
            return self.get_response(request)

        if request.method == 'GET':
            return self.get_response(request)

        if request.method == 'OPTIONS':
            return self.get_response(request)

        is_public = self._is_public_operation(request)
        if is_public:
            return self.get_response(request)

        auth_header = request.META.get('HTTP_AUTHORIZATION', '')

        if not auth_header.startswith('Bearer '):
            return JsonResponse(
                {'errors': [{'message': 'Authentication required'}]},
                status=401
            )

        token = auth_header.split(' ')[1]

        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=['HS256']
            )
            request.user_id = payload.get('user_id')

        except jwt.ExpiredSignatureError:
            return JsonResponse(
                {'errors': [
                    {'message': 'Token has expired. Please login again.'}]},
                status=401
            )
        except jwt.InvalidTokenError as e:
            return JsonResponse(
                {'errors': [{'message': 'Invalid token'}]},
                status=401
            )

        return self.get_response(request)

    def _is_public_operation(self, request):
        """Check if operation is public (login, register, etc.)"""
        try:
            if not hasattr(request, '_cached_body'):
                request._cached_body = request.body

            body = request._cached_body
            if not body:
                return False

            data = json.loads(body.decode('utf-8'))
            operation_name = data.get('operationName', '').lower()


            public_operations = [
                'userlogin',
                'login',
                'userregister',
                'register',
                'createuser',
                'signup',
                'forgetpassword',
                'resetpassword',
                'introspectionquery',
            ]

            is_public = operation_name in public_operations


            return is_public

        except Exception as e:
            print(f"⚠️ Auth middleware error: {e}")
            return False  # ✅ Fail secure