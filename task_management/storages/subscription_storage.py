from datetime import datetime
from typing import List, Optional

from django.utils import timezone

from task_management.exceptions.custom_exceptions import \
    SubscriptionNotFoundException
from task_management.interactors.dtos import PlanDTO, SubscriptionDTO
from task_management.interactors.storage_interfaces.subscription_storage_interface import (
    SubscriptionStorageInterface,
)
from task_management.models import Subscription


class SubscriptionStorage(SubscriptionStorageInterface):
    ACTIVE_STATUSES = ("active", "trialing", "past_due", "incomplete")

    def create_or_update_subscription(self,
                                      subscription_data: dict) -> SubscriptionDTO:
        defaults = {
            "user_id": subscription_data["user_id"],
            "plan_id": subscription_data["plan_id"],
            "status": subscription_data["status"],
            "current_period_start": subscription_data["current_period_start"],
            "current_period_end": subscription_data["current_period_end"],
            "cancel_at_period_end": subscription_data.get(
                "cancel_at_period_end", False),
            "canceled_at": subscription_data.get("canceled_at"),
        }
        subscription, _ = Subscription.objects.update_or_create(
            stripe_subscription_id=subscription_data["stripe_subscription_id"],
            defaults=defaults,
        )
        return self._convert_to_dto(subscription)

    def get_subscription_by_id(self, subscription_id: str) -> SubscriptionDTO:
        try:
            subscription = Subscription.objects.select_related("plan").get(
                subscription_id=subscription_id
            )
        except Subscription.DoesNotExist as exc:
            raise SubscriptionNotFoundException(
                subscription_id=subscription_id) from exc
        return self._convert_to_dto(subscription)

    def get_subscription_by_user_id(self, user_id: str) -> Optional[
        SubscriptionDTO]:
        subscription = (
            Subscription.objects.select_related("plan")
            .filter(user_id=user_id, status__in=self.ACTIVE_STATUSES)
            .order_by("-created_at")
            .first()
        )
        if subscription is None:
            return None
        return self._convert_to_dto(subscription)

    def get_subscription_by_stripe_id(
            self, stripe_subscription_id: str
    ) -> Optional[SubscriptionDTO]:
        try:
            subscription = Subscription.objects.select_related("plan").get(
                stripe_subscription_id=stripe_subscription_id
            )
        except Subscription.DoesNotExist:
            return None
        return self._convert_to_dto(subscription)

    def update_subscription_status(
            self,
            stripe_subscription_id: str,
            status: str,
            current_period_start,
            current_period_end,
            cancel_at_period_end: bool = False,
            canceled_at=None,
    ) -> SubscriptionDTO:
        try:
            subscription = Subscription.objects.get(
                stripe_subscription_id=stripe_subscription_id
            )
        except Subscription.DoesNotExist as exc:
            raise SubscriptionNotFoundException(
                subscription_id=stripe_subscription_id
            ) from exc
        subscription.status = status
        subscription.current_period_start = self._coerce_datetime(
            current_period_start)
        subscription.current_period_end = self._coerce_datetime(
            current_period_end)
        subscription.cancel_at_period_end = cancel_at_period_end
        subscription.canceled_at = self._coerce_datetime(
            canceled_at) if canceled_at else None
        subscription.save()
        return self._convert_to_dto(subscription)

    def schedule_subscription_cancellation(
            self, subscription_id: str, canceled_at
    ) -> SubscriptionDTO:
        subscription = Subscription.objects.get(
            subscription_id=subscription_id)
        subscription.cancel_at_period_end = True
        subscription.canceled_at = self._coerce_datetime(canceled_at)
        subscription.save(update_fields=["cancel_at_period_end", "canceled_at",
                                         "updated_at"])
        return self._convert_to_dto(subscription)

    def mark_subscription_canceled(
            self, stripe_subscription_id: str, canceled_at
    ) -> SubscriptionDTO:
        subscription = Subscription.objects.get(
            stripe_subscription_id=stripe_subscription_id
        )
        subscription.status = "canceled"
        subscription.cancel_at_period_end = False
        subscription.canceled_at = self._coerce_datetime(canceled_at)
        subscription.save()
        return self._convert_to_dto(subscription)

    def get_active_subscriptions(self, user_id: str) -> List[SubscriptionDTO]:
        subscriptions = Subscription.objects.select_related("plan").filter(
            user_id=user_id,
            status__in=self.ACTIVE_STATUSES,
        )
        return [self._convert_to_dto(subscription) for subscription in
                subscriptions]

    @staticmethod
    def _coerce_datetime(value):
        if value is None:
            return None
        if isinstance(value, datetime):
            if timezone.is_naive(value):
                return timezone.make_aware(value,
                                           timezone.get_current_timezone())
            return value
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        if timezone.is_naive(parsed):
            return timezone.make_aware(parsed, timezone.get_current_timezone())
        return parsed

    @staticmethod
    def _convert_to_dto(subscription: Subscription) -> SubscriptionDTO:
        plan_dto = None
        if subscription.plan:
            plan_dto = PlanDTO(
                plan_id=str(subscription.plan.plan_id),
                plan_name=subscription.plan.plan_name,
                stripe_price_id=subscription.plan.stripe_price_id,
                price=float(subscription.plan.price),
                currency=subscription.plan.currency,
                billing_period=subscription.plan.billing_period,
                features=subscription.plan.features,
                is_active=subscription.plan.is_active,
            )

        return SubscriptionDTO(
            subscription_id=str(subscription.subscription_id),
            user_id=str(subscription.user_id),
            plan=plan_dto,
            stripe_subscription_id=subscription.stripe_subscription_id,
            status=subscription.status,
            current_period_start=subscription.current_period_start,
            current_period_end=subscription.current_period_end,
            cancel_at_period_end=subscription.cancel_at_period_end,
            canceled_at=subscription.canceled_at,
        )
