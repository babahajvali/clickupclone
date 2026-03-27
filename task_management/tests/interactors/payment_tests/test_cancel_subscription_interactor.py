from unittest.mock import Mock

import pytest

from task_management.interactors.dtos import CancelSubscriptionDTO
from task_management.interactors.payments.cancel_subscription_interactor import (
    CancelSubscriptionInteractor,
)
from task_management.storages.subscription_storage import SubscriptionStorage
from task_management.tests.factories.storage_factory import SubscriptionFactory


@pytest.mark.django_db
def test_cancel_subscription_schedules_cancellation(monkeypatch):
    subscription = SubscriptionFactory(status="active",
                                       cancel_at_period_end=False)
    stripe_modify = Mock()
    monkeypatch.setattr(
        "task_management.interactors.cancel_subscription_interactor.stripe.Subscription.modify",
        stripe_modify,
    )

    interactor = CancelSubscriptionInteractor(
        subscription_storage=SubscriptionStorage())

    result = interactor.cancel_subscription(
        CancelSubscriptionDTO(
            user_id=str(subscription.user_id),
            subscription_id=str(subscription.subscription_id),
        )
    )

    subscription.refresh_from_db()
    stripe_modify.assert_called_once_with(
        subscription.stripe_subscription_id,
        cancel_at_period_end=True,
    )
    assert result.status == "active"
    assert subscription.status == "active"
    assert subscription.cancel_at_period_end is True
    assert subscription.canceled_at is not None
