# task_management/interactors/cancel_subscription_interactor.py

import stripe
from django.conf import settings
from datetime import datetime
from task_management.interactors.dtos import CancelSubscriptionDTO, \
    SubscriptionDTO
from task_management.interactors.storage_interface.subscription_storage_interface import \
    SubscriptionStorageInterface
from task_management.exceptions.custom_exceptions import (
    SubscriptionNotFoundException,
    InvalidSubscriptionOwnerException
)

stripe.api_key = settings.STRIPE_SECRET_KEY


class CancelSubscriptionInteractor:

    def __init__(self, subscription_storage: SubscriptionStorageInterface):
        self.subscription_storage = subscription_storage

    def cancel_subscription(self,
                            cancel_data: CancelSubscriptionDTO) -> SubscriptionDTO:
        """Cancel a user's subscription"""

        # Get subscription
        subscription = self.subscription_storage.get_subscription_by_id(
            subscription_id=cancel_data.subscription_id
        )

        # Verify ownership
        if subscription.user_id != cancel_data.user_id:
            raise InvalidSubscriptionOwnerException(
                user_id=cancel_data.user_id,
                subscription_id=cancel_data.subscription_id
            )

        # Cancel in Stripe (cancel at period end, not immediately)
        stripe.Subscription.modify(
            subscription.stripe_subscription_id,
            cancel_at_period_end=True
        )

        # Update in database
        return self.subscription_storage.cancel_subscription(
            subscription_id=cancel_data.subscription_id,
            canceled_at=datetime.now().isoformat()
        )
    