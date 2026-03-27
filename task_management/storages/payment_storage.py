from typing import List

from task_management.interactors.dtos import PaymentDTO
from task_management.interactors.storage_interface.payment_storage_interface import (
    PaymentStorageInterface,
)
from task_management.models import Payment


class PaymentStorage(PaymentStorageInterface):
    def create_or_update_payment(self, payment_data: dict) -> PaymentDTO:
        payment, _ = Payment.objects.update_or_create(
            stripe_payment_intent_id=payment_data["stripe_payment_intent_id"],
            defaults={
                "user_id": payment_data["user_id"],
                "subscription_id": payment_data.get("subscription_id"),
                "amount": payment_data["amount"],
                "currency": payment_data["currency"],
                "status": payment_data["status"],
                "payment_method": payment_data.get("payment_method"),
            },
        )
        return self._convert_to_dto(payment)

    def get_payments_by_user_id(self, user_id: str) -> List[PaymentDTO]:
        payments = Payment.objects.filter(user_id=user_id).order_by(
            "-created_at")
        return [self._convert_to_dto(payment) for payment in payments]

    def update_payment_status(self, stripe_payment_intent_id: str,
                              status: str) -> PaymentDTO:
        payment = Payment.objects.get(
            stripe_payment_intent_id=stripe_payment_intent_id)
        payment.status = status
        payment.save(update_fields=["status", "updated_at"])
        return self._convert_to_dto(payment)

    def get_payment_by_intent_id(self,
                                 stripe_payment_intent_id: str) -> PaymentDTO:
        payment = Payment.objects.get(
            stripe_payment_intent_id=stripe_payment_intent_id)
        return self._convert_to_dto(payment)

    @staticmethod
    def _convert_to_dto(payment: Payment) -> PaymentDTO:
        return PaymentDTO(
            payment_id=str(payment.payment_id),
            user_id=str(payment.user_id),
            subscription_id=str(
                payment.subscription_id) if payment.subscription_id else None,
            stripe_payment_intent_id=payment.stripe_payment_intent_id,
            amount=float(payment.amount),
            currency=payment.currency,
            status=payment.status,
            payment_method=payment.payment_method,
            created_at=payment.created_at,
        )
