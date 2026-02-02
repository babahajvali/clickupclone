import jwt
from django.conf import settings
from django.http import JsonResponse
import json


class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip non-GraphQL paths
        if not request.path.startswith('/graphql'):
            return self.get_response(request)

        # Allow GET requests (GraphiQL UI)
        if request.method == 'GET':
            return self.get_response(request)

        # Allow OPTIONS (CORS)
        if request.method == 'OPTIONS':
            return self.get_response(request)

        # Check if public operation
        if self._is_public_operation(request):
            return self.get_response(request)

        # Require authentication for protected operations
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')

        if not auth_header.startswith('Bearer '):
            return JsonResponse(
                {'errors': [{'message': 'Authentication required'}]},
                status=401
            )

        token = auth_header.split(' ')[1]

        try:
            # Decode and verify JWT
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=['HS256']
            )

            user_id = payload.get('user_id')

            # ✅ Set user_id on request
            request.user_id = user_id

        except jwt.ExpiredSignatureError:
            return JsonResponse(
                {'errors': [
                    {'message': 'Token has expired. Please login again.'}]},
                status=401
            )
        except jwt.InvalidTokenError:
            return JsonResponse(
                {'errors': [{'message': 'Invalid token'}]},
                status=401
            )

        return self.get_response(request)

    def _is_public_operation(self, request):
        """Check if operation is public"""
        try:
            if not hasattr(request, '_cached_body'):
                request._cached_body = request.body

            body = request._cached_body
            if not body:
                return False

            data = json.loads(body.decode('utf-8'))
            operation_name = data.get('operationName', '').lower()
            query = data.get('query', '').lower()

            public_operations = [
                'userlogin',
                'login',
                'userregister',
                'register',
                'createuser',
                'signup',
                'forgotpassword',
                'resetpassword',
                'createaccount',
            ]

            # Check operation name
            if operation_name in public_operations:
                return True

            # Check query content
            for op in public_operations:
                if f'{op}(' in query or f'{op}{{' in query:
                    return True

            # ✅ REMOVED: __type and __schema check
            # This was causing false positives!

            return False

        except Exception as e:
            print(f"⚠️ Auth middleware error: {e}")
            return False