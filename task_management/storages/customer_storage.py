from typing import Optional

from task_management.interactors.storage_interface.customer_storage_interface import (
    CustomerStorageInterface,
)
from task_management.models import Customer, User


class CustomerStorage(CustomerStorageInterface):
    def create_customer(self, user_id: str, stripe_customer_id: str) -> dict:
        user = User.objects.get(user_id=user_id)
        customer, _ = Customer.objects.update_or_create(
            user=user,
            defaults={"stripe_customer_id": stripe_customer_id},
        )
        return self._convert_to_dict(customer)

    def get_customer_by_user_id(self, user_id: str) -> Optional[dict]:
        try:
            customer = Customer.objects.get(user_id=user_id)
        except Customer.DoesNotExist:
            return None
        return self._convert_to_dict(customer)

    def get_customer_by_stripe_id(self, stripe_customer_id: str) -> Optional[dict]:
        try:
            customer = Customer.objects.get(stripe_customer_id=stripe_customer_id)
        except Customer.DoesNotExist:
            return None
        return self._convert_to_dict(customer)

    def update_payment_method(self, customer_id: str, payment_method: str) -> dict:
        customer = Customer.objects.get(customer_id=customer_id)
        customer.default_payment_method = payment_method
        customer.save(update_fields=["default_payment_method", "updated_at"])
        return self._convert_to_dict(customer)

    @staticmethod
    def _convert_to_dict(customer: Customer) -> dict:
        return {
            "customer_id": str(customer.customer_id),
            "user_id": str(customer.user_id),
            "stripe_customer_id": customer.stripe_customer_id,
            "default_payment_method": customer.default_payment_method,
        }
