import uuid
from contextlib import contextmanager
from functools import wraps

from django.core.cache import cache
from django_redis import get_redis_connection

from task_management.exceptions.custom_exceptions import \
    ResourceLockedException


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


unlock_script = """
                if redis.call("get", KEYS[1]) == ARGV[1] then
                    return redis.call("del", KEYS[1])
                else
                    return 0
                end
                """


@contextmanager
def redis_lock(lock_key: str, timeout: int = 10):
    redis_client = get_redis_connection("default")
    lock_value = str(uuid.uuid4())

    acquired = redis_client.set(
        lock_key,
        lock_value,
        nx=True,
        ex=timeout
    )

    if not acquired:
        raise ResourceLockedException(lock_key=lock_key)

    try:
        yield
    finally:

        redis_client.eval(unlock_script, 1, lock_key, lock_value)
