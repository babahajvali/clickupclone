from functools import wraps

from django.core.cache import cache


def interactor_cache(cache_name: str, timeout=60):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key_parts = [str(func.__name__)]

            for a in args[1:]:
                key_parts.append(str(a))

            for k, v in sorted(kwargs.items()):
                key_parts.append(f"{k}={v}")

            cache_key = f"storage:{cache_name}:" + ":".join(key_parts)

            cached = cache.get(cache_key)
            if cached is not None:
                return cached

            result = func(*args, **kwargs)
            cache.set(cache_key, result, timeout)
            return result

        return wrapper

    return decorator


def invalidate_interactor_cache(cache_name: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            pattern = f"storage:{cache_name}:*"
            cache.delete_pattern(pattern)

            return result

        return wrapper

    return decorator
