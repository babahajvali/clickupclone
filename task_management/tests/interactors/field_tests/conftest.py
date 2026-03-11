import pytest
from contextlib import contextmanager

from django.db.transaction import Atomic
from task_management.decorators import caching_decorators


class _DummyCache:
    def get(self, key):
        return None

    def set(self, key, value, timeout=None):
        return None

    def delete_pattern(self, pattern):
        return None


@contextmanager
def _dummy_redis_lock(*args, **kwargs):
    yield


@pytest.fixture(autouse=True)
def patch_interactor_cache(monkeypatch):
    monkeypatch.setattr(caching_decorators, "cache", _DummyCache())
    monkeypatch.setattr(caching_decorators, "redis_lock", _dummy_redis_lock)
    monkeypatch.setattr(
        "task_management.interactors.fields.create_field_interactor.redis_lock",
        _dummy_redis_lock,
    )
    monkeypatch.setattr(
        "task_management.interactors.fields.update_field_interactor.redis_lock",
        _dummy_redis_lock,
    )
    monkeypatch.setattr(
        "task_management.interactors.fields.reorder_field_interactor.redis_lock",
        _dummy_redis_lock,
    )


@pytest.fixture(autouse=True)
def patch_atomic_transaction(monkeypatch):
    monkeypatch.setattr(Atomic, "__enter__", lambda self: None)
    monkeypatch.setattr(Atomic, "__exit__", lambda self, exc_type, exc, tb: False)
