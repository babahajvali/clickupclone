import pytest

from task_management.decorators import caching_decorators
from django.db.transaction import Atomic


class _DummyCache:
    def get(self, key):
        return None

    def set(self, key, value, timeout=None):
        return None

    def delete_pattern(self, pattern):
        return None


@pytest.fixture(autouse=True)
def patch_interactor_cache(monkeypatch):
    monkeypatch.setattr(caching_decorators, "cache", _DummyCache())


@pytest.fixture(autouse=True)
def patch_atomic_transaction(monkeypatch):
    monkeypatch.setattr(Atomic, "__enter__", lambda self: None)
    monkeypatch.setattr(Atomic, "__exit__", lambda self, exc_type, exc, tb: False)
