import logging
from datetime import datetime, timezone as dt_timezone

import stripe
from django.conf import settings
from django.utils import timezone

from task_management.exceptions.custom_exceptions import StripeWebhookException
from task_management.interactors.storage_interface.payment_storage_interface import (
    PaymentStorageInterface,
)
from task_management.interactors.storage_interface.plan_storage_interface import (
    PlanStorageInterface,
)
from task_management.interactors.storage_interface.subscription_storage_interface import (
    SubscriptionStorageInterface,
)

stripe.api_key = settings.STRIPE_SECRET_KEY
logger = logging.getLogger(__name__)


class WebhookHandlerInteractor:
    def __init__(
            self,
            subscription_storage: SubscriptionStorageInterface,
            payment_storage: PaymentStorageInterface,
            plan_storage: PlanStorageInterface,
    ):
        self.subscription_storage = subscription_storage
        self.payment_storage = payment_storage
        self.plan_storage = plan_storage

    def handle_webhook_event(self, payload: bytes, sig_header: str) -> dict:
        try:
            event = stripe.Webhook.construct_event(
                payload,
                sig_header,
                settings.STRIPE_WEBHOOK_SECRET,
            )
        except ValueError as exc:
            logger.exception("Stripe webhook payload validation failed")
            raise StripeWebhookException(message="Invalid payload") from exc
        except stripe.error.SignatureVerificationError as exc:
            logger.exception("Stripe webhook signature verification failed")
            raise StripeWebhookException(message="Invalid signature") from exc

        event_type = event["type"]
        event_data = event["data"]["object"]

        handlers = {
            "checkout.session.completed": self._handle_checkout_completed,
            "customer.subscription.created": self._handle_subscription_created,
            "customer.subscription.updated": self._handle_subscription_updated,
            "customer.subscription.deleted": self._handle_subscription_deleted,
            "invoice.payment_succeeded": self._handle_payment_succeeded,
            "invoice.payment_failed": self._handle_payment_failed,
            "invoice_payment.paid": self._handle_invoice_payment_paid,
            "invoice_payment.payment_failed": self._handle_invoice_payment_failed,
        }

        handler = handlers.get(event_type)
        if handler is None:
            logger.warning("Unhandled Stripe webhook event_type=%s",
                           event_type)
            return {"status": "unhandled_event", "type": event_type}
        return handler(event_data)

    def _handle_checkout_completed(self, session):
        user_id = session.get("metadata", {}).get("user_id")
        stripe_subscription_id = session.get("subscription")

        if not user_id:
            return {"status": "error", "message": "No user_id in metadata"}
        if not stripe_subscription_id:
            return {"status": "error", "message": "No subscription in session"}

        stripe_subscription = stripe.Subscription.retrieve(
            stripe_subscription_id,
            expand=["items.data.price"],
        )
        subscription_dto = self._upsert_subscription_from_stripe(
            stripe_subscription,
            user_id=user_id,
        )

        if session.get("payment_status") == "paid":
            payment_intent_id = (
                session.get("payment_intent")
                or f"checkout_session_{session['id']}"
            )
            amount_total = session.get("amount_total")
            currency = session.get("currency")

            if amount_total is not None and currency:
                self.payment_storage.create_or_update_payment(
                    {
                        "user_id": user_id,
                        "subscription_id": subscription_dto.subscription_id,
                        "stripe_payment_intent_id": payment_intent_id,
                        "amount": amount_total / 100,
                        "currency": currency.upper(),
                        "status": "succeeded",
                        "payment_method": "card",
                    }
                )

        return {
            "status": "success",
            "message": "Checkout completed",
            "user_id": user_id,
            "subscription_id": stripe_subscription["id"],
        }

    def _handle_subscription_created(self, subscription):
        existing = self.subscription_storage.get_subscription_by_stripe_id(
            stripe_subscription_id=subscription["id"]
        )
        if existing:
            return {"status": "skipped",
                    "message": "Already created via checkout"}

        customer = stripe.Customer.retrieve(subscription["customer"])
        user_id = customer.get("metadata", {}).get("user_id")
        if not user_id:
            raise StripeWebhookException(
                message="No user_id in customer metadata")

        full_subscription = stripe.Subscription.retrieve(
            subscription["id"],
            expand=["items.data.price"],
        )
        self._upsert_subscription_from_stripe(full_subscription,
                                              user_id=user_id)

        return {
            "status": "success",
            "message": "Subscription created",
            "subscription_id": subscription["id"],
        }

    def _handle_subscription_updated(self, subscription):
        items = subscription.get("items", {}).get("data", [])
        if not items:
            raise StripeWebhookException(
                message="No items found in subscription")

        period_start, period_end = self._extract_period(subscription)

        self.subscription_storage.update_subscription_status(
            stripe_subscription_id=subscription["id"],
            status=subscription["status"],
            current_period_start=datetime.fromtimestamp(period_start,
                                                        tz=dt_timezone.utc),
            current_period_end=datetime.fromtimestamp(period_end,
                                                      tz=dt_timezone.utc),
            cancel_at_period_end=subscription.get("cancel_at_period_end",
                                                  False),
            canceled_at=(
                datetime.fromtimestamp(subscription["canceled_at"],
                                       tz=dt_timezone.utc)
                if subscription.get("canceled_at")
                else None
            ),
        )

        return {
            "status": "success",
            "message": "Subscription updated",
            "subscription_id": subscription["id"],
        }

    def _handle_subscription_deleted(self, subscription):
        canceled_at = subscription.get("canceled_at")
        self.subscription_storage.mark_subscription_canceled(
            stripe_subscription_id=subscription["id"],
            canceled_at=(
                datetime.fromtimestamp(canceled_at, tz=dt_timezone.utc)
                if canceled_at
                else timezone.now()
            ),
        )
        return {
            "status": "success",
            "message": "Subscription canceled",
            "subscription_id": subscription["id"],
        }

    def _handle_payment_succeeded(self, invoice):
        if not invoice.get("subscription"):
            return {"status": "skipped", "message": "No subscription attached"}

        subscription_obj = self.subscription_storage.get_subscription_by_stripe_id(
            stripe_subscription_id=invoice["subscription"]
        )
        if not subscription_obj:
            return {"status": "skipped",
                    "message": "Subscription not yet in DB"}

        payment_intent_id = invoice.get(
            "payment_intent") or f"inv_{invoice['id']}"

        self.payment_storage.create_or_update_payment({
            "user_id": subscription_obj.user_id,
            "subscription_id": subscription_obj.subscription_id,
            "stripe_payment_intent_id": payment_intent_id,
            "amount": invoice["amount_paid"] / 100,
            "currency": invoice["currency"].upper(),
            "status": "succeeded",
            "payment_method": "card",
        })

        return {
            "status": "success",
            "message": "Payment recorded",
            "payment_intent": payment_intent_id,
        }

    def _handle_payment_failed(self, invoice):
        if not invoice.get("subscription"):
            return {"status": "skipped", "message": "No subscription attached"}

        subscription_obj = self.subscription_storage.get_subscription_by_stripe_id(
            stripe_subscription_id=invoice["subscription"]
        )
        if not subscription_obj:
            return {"status": "skipped",
                    "message": "Subscription not yet in DB"}

        self.subscription_storage.update_subscription_status(
            stripe_subscription_id=invoice["subscription"],
            status="past_due",
            current_period_start=datetime.fromtimestamp(
                invoice["period_start"], tz=dt_timezone.utc,
            ),
            current_period_end=datetime.fromtimestamp(
                invoice["period_end"], tz=dt_timezone.utc,
            ),
            cancel_at_period_end=subscription_obj.cancel_at_period_end,
            canceled_at=subscription_obj.canceled_at,
        )

        payment_intent_id = invoice.get(
            "payment_intent") or f"failed_{invoice['id']}"
        self.payment_storage.create_or_update_payment({
            "user_id": subscription_obj.user_id,
            "subscription_id": subscription_obj.subscription_id,
            "stripe_payment_intent_id": payment_intent_id,
            "amount": invoice["amount_due"] / 100,
            "currency": invoice["currency"].upper(),
            "status": "failed",
            "payment_method": None,
        })

        return {
            "status": "success",
            "message": "Payment failure recorded",
            "invoice_id": invoice["id"],
        }

    def _handle_invoice_payment_paid(self, invoice_payment):
        stripe_subscription_id = invoice_payment.get("subscription")

        if not stripe_subscription_id:
            invoice_id = invoice_payment.get("invoice")
            if not invoice_id:
                return {"status": "skipped",
                        "message": "No subscription or invoice attached"}
            invoice = stripe.Invoice.retrieve(invoice_id)
            stripe_subscription_id = invoice.get("subscription")

        if not stripe_subscription_id:
            return {"status": "skipped", "message": "No subscription attached"}

        subscription_obj = self.subscription_storage.get_subscription_by_stripe_id(
            stripe_subscription_id=stripe_subscription_id
        )
        if not subscription_obj:
            return {"status": "skipped",
                    "message": "Subscription not yet in DB"}

        payment_intent_id = (
                invoice_payment.get("payment", {}).get("payment_intent")
                or f"inv_payment_{invoice_payment['id']}"
        )
        amount_paid = invoice_payment.get("amount_paid", 0)
        currency = invoice_payment.get("currency", "usd")

        self.payment_storage.create_or_update_payment({
            "user_id": subscription_obj.user_id,
            "subscription_id": subscription_obj.subscription_id,
            "stripe_payment_intent_id": payment_intent_id,
            "amount": amount_paid / 100,
            "currency": currency.upper(),
            "status": "succeeded",
            "payment_method": "card",
        })

        return {
            "status": "success",
            "message": "Payment recorded",
            "payment_intent": payment_intent_id,
        }

    def _handle_invoice_payment_failed(self, invoice_payment):
        stripe_subscription_id = invoice_payment.get("subscription")
        if not stripe_subscription_id:
            return {"status": "skipped", "message": "No subscription attached"}

        subscription_obj = self.subscription_storage.get_subscription_by_stripe_id(
            stripe_subscription_id=stripe_subscription_id
        )
        if not subscription_obj:
            return {"status": "skipped",
                    "message": "Subscription not yet in DB"}

        payment_intent_id = (
                invoice_payment.get("payment", {}).get("payment_intent")
                or f"inv_payment_failed_{invoice_payment['id']}"
        )
        amount_due = invoice_payment.get("amount_due", 0)
        currency = invoice_payment.get("currency", "usd")

        self.payment_storage.create_or_update_payment({
            "user_id": subscription_obj.user_id,
            "subscription_id": subscription_obj.subscription_id,
            "stripe_payment_intent_id": payment_intent_id,
            "amount": amount_due / 100,
            "currency": currency.upper(),
            "status": "failed",
            "payment_method": None,
        })

        return {"status": "success", "message": "Payment failure recorded"}

    def _extract_period(self, subscription):
        items = subscription.get("items", {}).get("data", [])
        period_start = (
                subscription.get("current_period_start")
                or (items[0].get("current_period_start") if items else None)
        )
        period_end = (
                subscription.get("current_period_end")
                or (items[0].get("current_period_end") if items else None)
        )

        if not period_start or not period_end:
            full_sub = stripe.Subscription.retrieve(
                subscription["id"],
                expand=["items.data.price"],
            )
            full_items = full_sub.get("items", {}).get("data", [])
            period_start = (
                    full_sub.get("current_period_start")
                    or (full_items[0].get(
                "current_period_start") if full_items else None)
            )
            period_end = (
                    full_sub.get("current_period_end")
                    or (full_items[0].get(
                "current_period_end") if full_items else None)
            )

        if not period_start or not period_end:
            raise StripeWebhookException(
                message=f"Cannot determine billing period for subscription {subscription['id']}"
            )

        return period_start, period_end

    def _upsert_subscription_from_stripe(self, subscription, user_id: str):
        items = subscription.get("items", {}).get("data", [])
        if not items:
            raise StripeWebhookException(
                message="No items found in subscription")

        stripe_price_id = items[0].get("price", {}).get("id")
        plan = self.plan_storage.get_plan_by_stripe_price_id(stripe_price_id)
        if not plan:
            raise StripeWebhookException(
                message=f"Plan not found for price_id: {stripe_price_id}"
            )

        period_start, period_end = self._extract_period(subscription)

        return self.subscription_storage.create_or_update_subscription(
            {
                "user_id": user_id,
                "plan_id": plan.plan_id,
                "stripe_subscription_id": subscription["id"],
                "status": subscription["status"],
                "current_period_start": datetime.fromtimestamp(
                    period_start, tz=dt_timezone.utc,
                ),
                "current_period_end": datetime.fromtimestamp(
                    period_end, tz=dt_timezone.utc,
                ),
                "cancel_at_period_end": subscription.get(
                    "cancel_at_period_end", False),
                "canceled_at": (
                    datetime.fromtimestamp(subscription["canceled_at"],
                                           tz=dt_timezone.utc)
                    if subscription.get("canceled_at")
                    else None
                ),
            }
        )
