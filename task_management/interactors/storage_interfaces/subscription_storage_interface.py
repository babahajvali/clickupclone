from abc import ABC, abstractmethod
from typing import List, Optional

from task_management.interactors.dtos import SubscriptionDTO


class SubscriptionStorageInterface(ABC):
    @abstractmethod
    def create_or_update_subscription(self, subscription_data: dict) -> SubscriptionDTO:
        pass

    @abstractmethod
    def get_subscription_by_id(self, subscription_id: str) -> SubscriptionDTO:
        pass

    @abstractmethod
    def get_subscription_by_user_id(self, user_id: str) -> Optional[SubscriptionDTO]:
        pass

    @abstractmethod
    def get_subscription_by_stripe_id(self, stripe_subscription_id: str) -> SubscriptionDTO:
        pass

    @abstractmethod
    def update_subscription_status(
        self,
        stripe_subscription_id: str,
        status: str,
        current_period_start,
        current_period_end,
        cancel_at_period_end: bool = False,
        canceled_at=None,
    ) -> SubscriptionDTO:
        pass

    @abstractmethod
    def schedule_subscription_cancellation(
        self,
        subscription_id: str,
        canceled_at,
    ) -> SubscriptionDTO:
        pass

    @abstractmethod
    def mark_subscription_canceled(
        self,
        stripe_subscription_id: str,
        canceled_at,
    ) -> SubscriptionDTO:
        pass

    @abstractmethod
    def get_active_subscriptions(self, user_id: str) -> List[SubscriptionDTO]:
        pass
