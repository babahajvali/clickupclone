import stripe
from django.conf import settings
from task_management.interactors.dtos import CreateCheckoutSessionDTO, \
    CheckoutSessionResponseDTO
from task_management.interactors.storage_interface.plan_storage_interface import \
    PlanStorageInterface
from task_management.interactors.storage_interface.customer_storage_interface import \
    CustomerStorageInterface
from task_management.exceptions.custom_exceptions import PlanNotFoundException, \
    StripeCheckoutException
from task_management.models import User

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckoutSessionInteractor:

    def __init__(self, plan_storage: PlanStorageInterface,
                 customer_storage: CustomerStorageInterface):
        self.plan_storage = plan_storage
        self.customer_storage = customer_storage

    def create_checkout_session(self,
                                checkout_data: CreateCheckoutSessionDTO) -> CheckoutSessionResponseDTO:
        # Get plan details
        plan = self.plan_storage.get_plan_by_id(plan_id=checkout_data.plan_id)

        if not plan:
            raise PlanNotFoundException(plan_id=checkout_data.plan_id)

        # Get or create Stripe customer
        customer = self.customer_storage.get_customer_by_user_id(
            user_id=checkout_data.user_id)

        if customer:
            stripe_customer_id = customer['stripe_customer_id']
        else:
            # Create new Stripe customer
            user = User.objects.get(user_id=checkout_data.user_id)
            stripe_customer = stripe.Customer.create(
                email=user.email,
                metadata={'user_id': str(user.user_id)}
            )
            stripe_customer_id = stripe_customer.id

            # Save to database
            self.customer_storage.create_customer(
                user_id=checkout_data.user_id,
                stripe_customer_id=stripe_customer_id
            )

        # Set default URLs if not provided
        success_url = checkout_data.success_url or settings.STRIPE_SUCCESS_URL
        cancel_url = checkout_data.cancel_url or settings.STRIPE_CANCEL_URL

        try:
            # Create Stripe checkout session
            checkout_session = stripe.checkout.Session.create(
                customer=stripe_customer_id,
                payment_method_types=['card'],
                line_items=[{
                    'price': plan.stripe_price_id,
                    'quantity': 1,
                }],
                mode='subscription',
                success_url=success_url + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=cancel_url,
                metadata={
                    'user_id': str(checkout_data.user_id),
                    'plan_id': str(checkout_data.plan_id)
                }
            )

            return CheckoutSessionResponseDTO(
                session_id=checkout_session.id,
                checkout_url=checkout_session.url
            )

        except stripe.error.StripeError as e:
            raise StripeCheckoutException(message=str(e))