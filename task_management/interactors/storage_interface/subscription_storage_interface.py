# task_management/interactors/storage_interface/subscription_storage_interface.py

from abc import ABC, abstractmethod
from typing import Optional, List
from task_management.interactors.dtos import SubscriptionDTO


class SubscriptionStorageInterface(ABC):

    @abstractmethod
    def create_subscription(self, subscription_data: dict) -> SubscriptionDTO:
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
    def update_subscription_status(self, stripe_subscription_id: str, status: str,
                                   current_period_start: str, current_period_end: str) -> SubscriptionDTO:
        pass

    @abstractmethod
    def cancel_subscription(self, subscription_id: str, canceled_at: str) -> SubscriptionDTO:
        pass

    @abstractmethod
    def get_active_subscriptions(self, user_id: str) -> List[SubscriptionDTO]:
        pass