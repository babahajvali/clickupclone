# task_management/interactors/storage_interface/payment_storage_interface.py

from abc import ABC, abstractmethod
from typing import List
from task_management.interactors.dtos import PaymentDTO


class PaymentStorageInterface(ABC):

    @abstractmethod
    def create_payment(self, payment_data: dict) -> PaymentDTO:
        pass

    @abstractmethod
    def get_payments_by_user_id(self, user_id: str) -> List[PaymentDTO]:
        pass

    @abstractmethod
    def update_payment_status(self, stripe_payment_intent_id: str, status: str) -> PaymentDTO:
        pass

    @abstractmethod
    def get_payment_by_intent_id(self, stripe_payment_intent_id: str) -> PaymentDTO:
        pass