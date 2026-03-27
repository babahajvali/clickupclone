import json

import pytest

from task_management.interactors.webhook_handler_interactor import (
    WebhookHandlerInteractor,
)
from task_management.models import Subscription
from task_management.storages.payment_storage import PaymentStorage
from task_management.storages.plan_storage import PlanStorage
from task_management.storages.subscription_storage import SubscriptionStorage
from task_management.tests.factories.storage_factory import (
    PlanFactory,
    SubscriptionFactory,
    UserFactory,
)


def _build_handler():
    return WebhookHandlerInteractor(
        subscription_storage=SubscriptionStorage(),
        payment_storage=PaymentStorage(),
        plan_storage=PlanStorage(),
    )


@pytest.mark.django_db
def test_invoice_payment_succeeded_is_idempotent(monkeypatch):
    subscription = SubscriptionFactory(stripe_subscription_id="sub_invoice")
    event = {
        "type": "invoice.payment_succeeded",
        "data": {
            "object": {
                "id": "in_123",
                "subscription": "sub_invoice",
                "payment_intent": "pi_123",
                "amount_paid": 999,
                "currency": "usd",
            }
        },
    }
    monkeypatch.setattr(
        "task_management.interactors.webhook_handler_interactor.stripe.Webhook.construct_event",
        lambda payload, sig_header, secret: event,
    )
    handler = _build_handler()

    first = handler.handle_webhook_event(json.dumps(event), "sig")
    second = handler.handle_webhook_event(json.dumps(event), "sig")

    subscription.refresh_from_db()
    assert first["status"] == "success"
    assert second["status"] == "success"
    assert subscription.payments.count() == 1
    assert subscription.payments.get().stripe_payment_intent_id == "pi_123"


@pytest.mark.django_db
def test_subscription_created_is_idempotent(monkeypatch):
    user = UserFactory()
    plan = PlanFactory(stripe_price_id="price_pro")
    event = {
        "type": "customer.subscription.created",
        "data": {
            "object": {
                "id": "sub_created",
                "customer": "cus_123",
                "status": "active",
                "cancel_at_period_end": False,
                "items": {
                    "data": [
                        {
                            "price": {"id": "price_pro"},
                            "current_period_start": 1700000000,
                            "current_period_end": 1702592000,
                        }
                    ]
                },
            }
        },
    }
    monkeypatch.setattr(
        "task_management.interactors.webhook_handler_interactor.stripe.Webhook.construct_event",
        lambda payload, sig_header, secret: event,
    )
    monkeypatch.setattr(
        "task_management.interactors.webhook_handler_interactor.stripe.Customer.retrieve",
        lambda customer_id: {"id": customer_id, "metadata": {"user_id": str(user.user_id)}},
    )
    monkeypatch.setattr(
        "task_management.interactors.webhook_handler_interactor.stripe.Subscription.retrieve",
        lambda subscription_id, expand=None: event["data"]["object"],
    )
    handler = _build_handler()

    first = handler.handle_webhook_event(json.dumps(event), "sig")
    second = handler.handle_webhook_event(json.dumps(event), "sig")

    assert first["status"] == "success"
    assert second["status"] == "skipped"
    assert Subscription.objects.filter(stripe_subscription_id="sub_created").count() == 1
    created_subscription = Subscription.objects.get(stripe_subscription_id="sub_created")
    assert created_subscription.user_id == user.user_id
    assert created_subscription.plan_id == plan.plan_id


@pytest.mark.django_db
def test_checkout_completed_creates_initial_payment(monkeypatch):
    user = UserFactory()
    PlanFactory(stripe_price_id="price_checkout")
    event = {
        "type": "checkout.session.completed",
        "data": {
            "object": {
                "id": "cs_123",
                "subscription": "sub_checkout",
                "payment_status": "paid",
                "payment_intent": "pi_checkout",
                "amount_total": 1999,
                "currency": "usd",
                "metadata": {"user_id": str(user.user_id)},
            }
        },
    }
    stripe_subscription = {
        "id": "sub_checkout",
        "status": "active",
        "cancel_at_period_end": False,
        "items": {
            "data": [
                {
                    "price": {"id": "price_checkout"},
                    "current_period_start": 1700000000,
                    "current_period_end": 1702592000,
                }
            ]
        },
    }
    monkeypatch.setattr(
        "task_management.interactors.webhook_handler_interactor.stripe.Webhook.construct_event",
        lambda payload, sig_header, secret: event,
    )
    monkeypatch.setattr(
        "task_management.interactors.webhook_handler_interactor.stripe.Subscription.retrieve",
        lambda subscription_id, expand=None: stripe_subscription,
    )

    handler = _build_handler()
    result = handler.handle_webhook_event(json.dumps(event), "sig")

    assert result["status"] == "success"
    subscription = Subscription.objects.get(stripe_subscription_id="sub_checkout")
    assert subscription.payments.count() == 1
    payment = subscription.payments.get()
    assert payment.stripe_payment_intent_id == "pi_checkout"
    assert float(payment.amount) == 19.99
    assert payment.status == "succeeded"
