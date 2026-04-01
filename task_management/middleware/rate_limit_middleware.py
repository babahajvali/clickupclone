import json

from django.core.cache import cache
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

RATE_LIMIT = 5
WINDOW_SIZE = 2
COOLDOWN_PERIOD = 60


class RateLimitMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if not request.path.startswith("/graphql"):
            return None

        try:
            data = json.loads(request.body.decode("utf-8"))
        except json.JSONDecodeError:
            return None

        operation_name = data.get("operationName")

        if operation_name != "UserLogin":
            return None

        identifier = self._get_identifier(request, data)

        block_key = f"rl:block:{identifier}"
        counter_key = f"rl:count:{identifier}"

        if cache.get(block_key):
            retry_after = self._get_ttl(block_key) or COOLDOWN_PERIOD
            return self.too_many_requests_response(retry_after)

        try:
            current_count = cache.incr(counter_key)
        except ValueError:
            cache.set(counter_key, 1, timeout=WINDOW_SIZE)
            current_count = 1

        if current_count > RATE_LIMIT:
            cache.set(block_key, 1, timeout=COOLDOWN_PERIOD)
            cache.delete(counter_key)
            return self.too_many_requests_response(COOLDOWN_PERIOD)

        return None

    def _get_identifier(self, request, data):
        ip = self._get_ip(request)
        variables = data.get("variables", {}) or {}

        username = (
                variables.get("username")
                or variables.get("email")
                or "anonymous"
        )

        return f"{username}:{ip}"

    @staticmethod
    def _get_ip(request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")

        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()

        return request.META.get("REMOTE_ADDR", "unknown")

    @staticmethod
    def _get_ttl(key):
        try:
            return cache.ttl(key)
        except Exception:
            return None

    @staticmethod
    def too_many_requests_response(retry_after_seconds):
        response = JsonResponse(
            {
                "error": "Too Many Requests",
                "message": "Too many login attempts. Try again later.",
                "retry_after_seconds": retry_after_seconds,
            },
            status=429,
        )
        response["Retry-After"] = str(retry_after_seconds)
        return response
