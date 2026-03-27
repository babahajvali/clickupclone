from types import SimpleNamespace

import pytest

from task_management.graphql.subscription_queries import SubscriptionQueries
from task_management.tests.factories.storage_factory import SubscriptionFactory


@pytest.mark.django_db
def test_get_my_subscription_resolver_uses_context_user_id():
    subscription = SubscriptionFactory(status="active")
    info = SimpleNamespace(context=SimpleNamespace(user_id=str(subscription.user_id)))

    result = SubscriptionQueries.resolve_get_my_subscription(None, info)

    assert result.subscription_id == subscription.subscription_id
