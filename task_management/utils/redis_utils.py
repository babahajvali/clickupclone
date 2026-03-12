import uuid
from contextlib import contextmanager

from django_redis import get_redis_connection

from task_management.exceptions.custom_exceptions import \
    ResourceLockedException

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
