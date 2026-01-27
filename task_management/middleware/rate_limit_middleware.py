import json
import time
from django.http import JsonResponse
from django.core.cache import cache

RATE_LIMIT = 5
WINDOW_SIZE = 2  # seconds
COOLDOWN_PERIOD = 60  # seconds


class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.path.startswith("/graphql"):
            return self.get_response(request)

        try:
            data = json.loads(request.body.decode("utf-8"))
            query = data.get("query", "")
        except Exception:
            return self.get_response(request)

        if "userLogin" not in query:
            return self.get_response(request)

        if hasattr(request, "user") and request.user.is_authenticated:
            identifier = f"user:{request.user.id}"
        else:
            identifier = f"ip:{self._get_ip(request)}"

        block_key = f"rl:login:block:{identifier}"
        window_key = f"rl:login:window:{identifier}"

        if cache.get(block_key):
            retry_after = cache.ttl(block_key) or COOLDOWN_PERIOD
            return self.too_many_requests_response(retry_after)

        now = time.time()

        timestamps = cache.get(window_key) or []

        cutoff = now - WINDOW_SIZE
        timestamps = [ts for ts in timestamps if ts > cutoff]

        if len(timestamps) >= RATE_LIMIT:

            cache.set(block_key, 1, timeout=COOLDOWN_PERIOD)
            cache.delete(window_key)
            return self.too_many_requests_response(COOLDOWN_PERIOD)

        timestamps.append(now)
        cache.set(window_key, timestamps, timeout=WINDOW_SIZE)

        return self.get_response(request)

    @staticmethod
    def _get_ip(request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR")

    @staticmethod
    def too_many_requests_response(retry_after_seconds):
        response = JsonResponse(
            {
                "error": "Too Many Requests",
                "message": "You have exceeded the rate limit for login attempts.",
                "retry_after_seconds": retry_after_seconds,
            },
            status=429,
        )
        response["Retry-After"] = str(retry_after_seconds)
        return response