# task_management/storages/customer_storage.py
from sqlite3 import IntegrityError

from task_management.interactors.storage_interface.customer_storage_interface import \
    CustomerStorageInterface
from task_management.models import Customer, User
from typing import Optional


class CustomerStorage(CustomerStorageInterface):

    def create_customer(self, user_id: str, stripe_customer_id: str) -> dict:
        print(f"Looking for user_id: {user_id}")

        try:
            user = User.objects.get(user_id=user_id)
            print(f"✅ User found: {user.username} ({user.email})")
            print(f"   User PK type: {type(user.pk)}")
            print(f"   User PK value: {user.pk}")
        except User.DoesNotExist:
            print(f"❌ User with user_id={user_id} does NOT exist in database!")
            raise

        # Check if customer already exists
        try:
            existing_customer = Customer.objects.get(user=user)
            print(f"⚠️ Customer already exists for this user")
            existing_customer.stripe_customer_id = stripe_customer_id
            existing_customer.save()
            print(f"✅ Updated existing customer")
            return self._convert_to_dict(existing_customer)
        except Customer.DoesNotExist:
            print(f"Creating new customer...")

        try:
            # Create new customer - EXPLICIT field assignment
            customer = Customer(
                user=user,  # Pass the user object directly
                stripe_customer_id=stripe_customer_id
            )
            customer.save()

            print(f"✅ Customer created successfully")
            print(f"   Customer ID: {customer.customer_id}")
            print(f"   Stripe Customer ID: {customer.stripe_customer_id}")

            return self._convert_to_dict(customer)

        except IntegrityError as e:
            print(f"❌ IntegrityError: {str(e)}")
            # Try to show more details
            from django.db import connection
            print(
                f"   Last query: {connection.queries[-1] if connection.queries else 'None'}")
            raise
        except Exception as e:
            print(f"❌ Error creating customer: {type(e).__name__}: {str(e)}")
            raise

    def get_customer_by_user_id(self, user_id: str) -> Optional[dict]:
        try:
            customer = Customer.objects.get(user_id=user_id)
            return self._convert_to_dict(customer)
        except Customer.DoesNotExist:
            print("Hajvali")
            return None

    def get_customer_by_stripe_id(self, stripe_customer_id: str) -> Optional[dict]:
        try:
            customer = Customer.objects.get(stripe_customer_id=stripe_customer_id)
            return self._convert_to_dict(customer)
        except Customer.DoesNotExist:
            return None

    def update_payment_method(self, customer_id: str, payment_method: str) -> dict:
        customer = Customer.objects.get(customer_id=customer_id)
        customer.default_payment_method = payment_method
        customer.save()
        return self._convert_to_dict(customer)

    @staticmethod
    def _convert_to_dict(customer: Customer) -> dict:
        return {
            'customer_id': str(customer.customer_id),
            'user_id': str(customer.user_id),
            'stripe_customer_id': customer.stripe_customer_id,
            'default_payment_method': customer.default_payment_method,
        }