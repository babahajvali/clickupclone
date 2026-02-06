# task_management/interactors/get_payment_history_interactor.py

from typing import List
from task_management.interactors.dtos import PaymentDTO
from task_management.interactors.storage_interface.payment_storage_interface import PaymentStorageInterface


class GetPaymentHistoryInteractor:

    def __init__(self, payment_storage: PaymentStorageInterface):
        self.payment_storage = payment_storage

    def get_user_payments(self, user_id: str) -> List[PaymentDTO]:
        """Get payment history for a user"""
        return self.payment_storage.get_payments_by_user_id(user_id=user_id)