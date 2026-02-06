# task_management/storages/subscription_storage.py

from task_management.interactors.storage_interface.subscription_storage_interface import \
    SubscriptionStorageInterface
from task_management.models import Subscription, Plan
from task_management.interactors.dtos import SubscriptionDTO, PlanDTO
from task_management.exceptions.custom_exceptions import \
    SubscriptionNotFoundException
from typing import Optional, List
from datetime import datetime


class SubscriptionStorage(SubscriptionStorageInterface):

    def create_subscription(self, subscription_data: dict) -> SubscriptionDTO:
        subscription = Subscription.objects.create(**subscription_data)
        return self._convert_to_dto(subscription)

    def get_subscription_by_id(self, subscription_id: str) -> SubscriptionDTO:
        try:
            subscription = Subscription.objects.select_related('plan').get(
                subscription_id=subscription_id
            )
            return self._convert_to_dto(subscription)
        except Subscription.DoesNotExist:
            raise SubscriptionNotFoundException(
                subscription_id=subscription_id)

    def get_subscription_by_user_id(self, user_id: str) -> Optional[
        SubscriptionDTO]:
        try:
            subscription = Subscription.objects.select_related('plan').filter(
                user_id=user_id,
                status='active'
            ).order_by('-created_at').first()

            if subscription:
                return self._convert_to_dto(subscription)
            return None
        except Subscription.DoesNotExist:
            return None

    def get_subscription_by_stripe_id(self,
                                      stripe_subscription_id: str) -> SubscriptionDTO:
        try:
            subscription = Subscription.objects.select_related('plan').get(
                stripe_subscription_id=stripe_subscription_id
            )
            return self._convert_to_dto(subscription)
        except Subscription.DoesNotExist:
            raise SubscriptionNotFoundException(
                subscription_id=stripe_subscription_id)

    def update_subscription_status(self, stripe_subscription_id: str,
                                   status: str,
                                   current_period_start: str,
                                   current_period_end: str) -> SubscriptionDTO:
        subscription = Subscription.objects.get(
            stripe_subscription_id=stripe_subscription_id)
        subscription.status = status
        subscription.current_period_start = datetime.fromisoformat(
            current_period_start.replace('Z', '+00:00'))
        subscription.current_period_end = datetime.fromisoformat(
            current_period_end.replace('Z', '+00:00'))
        subscription.save()

        return self._convert_to_dto(subscription)

    def cancel_subscription(self, subscription_id: str,
                            canceled_at: str) -> SubscriptionDTO:
        subscription = Subscription.objects.get(
            subscription_id=subscription_id)
        subscription.status = 'canceled'
        subscription.cancel_at_period_end = True
        subscription.canceled_at = datetime.fromisoformat(
            canceled_at.replace('Z', '+00:00'))
        subscription.save()

        return self._convert_to_dto(subscription)

    def get_active_subscriptions(self, user_id: str) -> List[SubscriptionDTO]:
        subscriptions = Subscription.objects.select_related('plan').filter(
            user_id=user_id,
            status='active'
        )
        return [self._convert_to_dto(sub) for sub in subscriptions]

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
                is_active=subscription.plan.is_active
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
            canceled_at=subscription.canceled_at
        )