# task_management/interactors/get_subscription_details_interactor.py

from typing import Optional
from task_management.interactors.dtos import SubscriptionDTO
from task_management.interactors.storage_interface.subscription_storage_interface import SubscriptionStorageInterface


class GetSubscriptionDetailsInteractor:

    def __init__(self, subscription_storage: SubscriptionStorageInterface):
        self.subscription_storage = subscription_storage

    def get_user_subscription(self, user_id: str) -> Optional[SubscriptionDTO]:
        """Get active subscription for a user"""
        return self.subscription_storage.get_subscription_by_user_id(user_id=user_id)