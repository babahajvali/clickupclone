import stripe
from django.conf import settings
from django.utils import timezone

from task_management.exceptions.custom_exceptions import (
    InvalidSubscriptionOwnerException,
)
from task_management.interactors.dtos import CancelSubscriptionDTO, \
    SubscriptionDTO
from task_management.interactors.storage_interfaces.subscription_storage_interface import (
    SubscriptionStorageInterface,
)

stripe.api_key = settings.STRIPE_SECRET_KEY


class CancelSubscriptionInteractor:
    def __init__(self, subscription_storage: SubscriptionStorageInterface):
        self.subscription_storage = subscription_storage

    def cancel_subscription(self,
                            cancel_data: CancelSubscriptionDTO) -> SubscriptionDTO:
        subscription = self.subscription_storage.get_subscription_by_id(
            subscription_id=cancel_data.subscription_id
        )

        if subscription.user_id != cancel_data.user_id:
            raise InvalidSubscriptionOwnerException(
                user_id=cancel_data.user_id,
                subscription_id=cancel_data.subscription_id,
            )

        stripe.Subscription.modify(
            subscription.stripe_subscription_id,
            cancel_at_period_end=True,
        )

        return self.subscription_storage.schedule_subscription_cancellation(
            subscription_id=cancel_data.subscription_id,
            canceled_at=timezone.now(),
        )
