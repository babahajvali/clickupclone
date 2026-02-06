# task_management/interactors/storage_interface/customer_storage_interface.py

from abc import ABC, abstractmethod
from typing import Optional


class CustomerStorageInterface(ABC):

    @abstractmethod
    def create_customer(self, user_id: str, stripe_customer_id: str) -> dict:
        pass

    @abstractmethod
    def get_customer_by_user_id(self, user_id: str) -> Optional[dict]:
        pass

    @abstractmethod
    def get_customer_by_stripe_id(self, stripe_customer_id: str) -> Optional[dict]:
        pass

    @abstractmethod
    def update_payment_method(self, customer_id: str, payment_method: str) -> dict:
        pass