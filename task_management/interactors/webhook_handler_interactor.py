# task_management/interactors/webhook_handler_interactor.py

import stripe
from django.conf import settings
from datetime import datetime
from task_management.interactors.dtos import WebhookEventDTO
from task_management.interactors.storage_interface.subscription_storage_interface import \
    SubscriptionStorageInterface
from task_management.interactors.storage_interface.payment_storage_interface import \
    PaymentStorageInterface
from task_management.interactors.storage_interface.plan_storage_interface import \
    PlanStorageInterface
from task_management.exceptions.custom_exceptions import StripeWebhookException

stripe.api_key = settings.STRIPE_SECRET_KEY


class WebhookHandlerInteractor:

    def __init__(self, subscription_storage: SubscriptionStorageInterface,
                 payment_storage: PaymentStorageInterface,
                 plan_storage: PlanStorageInterface):
        self.subscription_storage = subscription_storage
        self.payment_storage = payment_storage
        self.plan_storage = plan_storage

    def handle_webhook_event(self, payload: str, sig_header: str) -> dict:
        """Verify and process webhook event from Stripe"""

        try:
            # Verify webhook signature
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except ValueError:
            raise StripeWebhookException(message="Invalid payload")
        except stripe.error.SignatureVerificationError:
            raise StripeWebhookException(message="Invalid signature")

        # Handle different event types
        event_type = event['type']
        event_data = event['data']['object']


        if event_type == 'checkout.session.completed':
            return self._handle_checkout_completed(event_data)

        elif event_type == 'customer.subscription.created':
            return self._handle_subscription_created(event_data)

        elif event_type == 'customer.subscription.updated':
            return self._handle_subscription_updated(event_data)

        elif event_type == 'customer.subscription.deleted':
            return self._handle_subscription_deleted(event_data)

        elif event_type == 'invoice.payment_succeeded':
            return self._handle_payment_succeeded(event_data)

        elif event_type == 'invoice.payment_failed':
            return self._handle_payment_failed(event_data)

        else:
            return {'status': 'unhandled_event', 'type': event_type}

    def _handle_checkout_completed(self, session):
        """Handle successful checkout session"""

        user_id = session.get('metadata', {}).get('user_id')
        plan_id = session.get('metadata', {}).get('plan_id')

        if not user_id:
            return {'status': 'error', 'message': 'No user_id in metadata'}

        # Get the Stripe subscription ID from the session
        stripe_subscription_id = session.get('subscription')
        if not stripe_subscription_id:
            return {'status': 'error', 'message': 'No subscription in session'}

        # Retrieve the full subscription details from Stripe
        try:
            stripe_subscription = stripe.Subscription.retrieve(
                stripe_subscription_id)
        except Exception as e:
            raise

        # Get plan from Stripe price ID
        items = stripe_subscription.get('items', {}).get('data', [])
        if not items:
            raise StripeWebhookException(
                message="No items found in subscription")

        stripe_price_id = items[0].get('price', {}).get('id')
        plan = self.plan_storage.get_plan_by_stripe_price_id(stripe_price_id)

        if not plan:
            raise StripeWebhookException(
                message=f"Plan not found for price_id: {stripe_price_id}")

        # Get period dates from subscription
        subscription_item = items[0]
        current_period_start = subscription_item.get('current_period_start')
        current_period_end = subscription_item.get('current_period_end')

        # Create subscription in database (if not already created)
        subscription_data = {
            'user_id': user_id,
            'plan_id': plan.plan_id,
            'stripe_subscription_id': stripe_subscription.id,
            'status': stripe_subscription.status,
            'current_period_start': datetime.fromtimestamp(
                current_period_start),
            'current_period_end': datetime.fromtimestamp(current_period_end),
        }

        try:
            subscription_obj = self.subscription_storage.create_subscription(
                subscription_data)
        except Exception as e:
            # If subscription already exists (created by customer.subscription.created event)
            subscription_obj = self.subscription_storage.get_subscription_by_stripe_id(
                stripe_subscription_id=stripe_subscription.id
            )

        # 🎯 CREATE THE INITIAL PAYMENT HERE
        if session.get('payment_status') == 'paid':
            payment_intent_id = session.get('payment_intent')

            if not payment_intent_id:
                payment_intent_id = f"cs_{session['id']}"

            payment_data = {
                'user_id': user_id,
                'subscription_id': subscription_obj.subscription_id,
                'stripe_payment_intent_id': payment_intent_id,
                'amount': session['amount_total'] / 100,
                # Convert from cents to dollars
                'currency': session['currency'].upper(),
                'status': 'succeeded',
                'payment_method': 'card'
            }

            try:
                payment = self.payment_storage.create_payment(payment_data)
            except Exception as e:
                import traceback
                traceback.print_exc()
                # Don't raise - we still want to acknowledge the webhook

        return {
            'status': 'success',
            'message': 'Checkout completed, subscription and payment created',
            'user_id': user_id,
            'subscription_id': stripe_subscription.id
        }

    def _handle_subscription_created(self, subscription):
        """Handle new subscription creation"""

        # Get plan from Stripe price ID
        items = subscription.get('items', {}).get('data', [])
        if not items:
            raise StripeWebhookException(
                message="No items found in subscription")

        stripe_price_id = items[0].get('price', {}).get('id')
        plan = self.plan_storage.get_plan_by_stripe_price_id(stripe_price_id)

        if not plan:
            raise StripeWebhookException(
                message=f"Plan not found for price_id: {stripe_price_id}")

        # Get user_id from customer metadata
        customer = stripe.Customer.retrieve(subscription['customer'])
        user_id = customer.get('metadata', {}).get('user_id')

        if not user_id:
            raise StripeWebhookException(
                message="No user_id in customer metadata")

        # Get period dates from subscription item
        subscription_item = items[0]
        current_period_start = subscription_item.get('current_period_start')
        current_period_end = subscription_item.get('current_period_end')

        # Create subscription in database
        subscription_data = {
            'user_id': user_id,
            'plan_id': plan.plan_id,
            'stripe_subscription_id': subscription['id'],
            'status': subscription['status'],
            'current_period_start': datetime.fromtimestamp(
                current_period_start),
            'current_period_end': datetime.fromtimestamp(current_period_end),
        }

        self.subscription_storage.create_subscription(subscription_data)

        return {
            'status': 'success',
            'message': 'Subscription created',
            'subscription_id': subscription['id']
        }

    def _handle_subscription_updated(self, subscription):
        """Handle subscription updates (renewals, upgrades, etc.)"""

        self.subscription_storage.update_subscription_status(
            stripe_subscription_id=subscription['id'],
            status=subscription['status'],
            current_period_start=datetime.fromtimestamp(
                subscription['current_period_start']).isoformat(),
            current_period_end=datetime.fromtimestamp(
                subscription['current_period_end']).isoformat()
        )

        return {
            'status': 'success',
            'message': 'Subscription updated',
            'subscription_id': subscription['id']
        }

    def _handle_subscription_deleted(self, subscription):
        """Handle subscription cancellation"""

        subscription_obj = self.subscription_storage.get_subscription_by_stripe_id(
            stripe_subscription_id=subscription['id']
        )

        self.subscription_storage.cancel_subscription(
            subscription_id=subscription_obj.subscription_id,
            canceled_at=datetime.now().isoformat()
        )

        return {
            'status': 'success',
            'message': 'Subscription canceled',
            'subscription_id': subscription['id']
        }

    def _handle_payment_succeeded(self, invoice):
        """Handle successful payment"""

        # Get subscription
        if not invoice.get('subscription'):
            return {'status': 'skipped', 'message': 'No subscription attached'}

        try:
            subscription_obj = self.subscription_storage.get_subscription_by_stripe_id(
                stripe_subscription_id=invoice['subscription']
            )
        except Exception as e:
            raise

        # Create payment record
        payment_intent_id = invoice.get(
            'payment_intent') or f"inv_{invoice['id']}"

        payment_data = {
            'user_id': subscription_obj.user_id,
            'subscription_id': subscription_obj.subscription_id,
            'stripe_payment_intent_id': payment_intent_id,
            'amount': invoice['amount_paid'] / 100,  # Convert from cents
            'currency': invoice['currency'].upper(),
            'status': 'succeeded',
            'payment_method': invoice.get('payment_method_types', [None])[
                0] if invoice.get('payment_method_types') else 'card'
        }


        try:
            payment = self.payment_storage.create_payment(payment_data)
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise

        return {
            'status': 'success',
            'message': 'Payment recorded',
            'payment_intent': invoice.get('payment_intent')
        }

    def _handle_payment_failed(self, invoice):
        """Handle failed payment"""

        if not invoice.get('subscription'):
            return {'status': 'skipped', 'message': 'No subscription attached'}

        subscription_obj = self.subscription_storage.get_subscription_by_stripe_id(
            stripe_subscription_id=invoice['subscription']
        )

        # Update subscription status
        self.subscription_storage.update_subscription_status(
            stripe_subscription_id=invoice['subscription'],
            status='past_due',
            current_period_start=datetime.fromtimestamp(
                invoice['period_start']).isoformat(),
            current_period_end=datetime.fromtimestamp(
                invoice['period_end']).isoformat()
        )

        # Create failed payment record
        payment_data = {
            'user_id': subscription_obj.user_id,
            'subscription_id': subscription_obj.subscription_id,
            'stripe_payment_intent_id': invoice.get(
                'payment_intent') or f"failed_{invoice['id']}",
            'amount': invoice['amount_due'] / 100,
            'currency': invoice['currency'].upper(),
            'status': 'failed',
            'payment_method': None
        }

        self.payment_storage.create_payment(payment_data)

        return {
            'status': 'success',
            'message': 'Payment failure recorded',
            'invoice_id': invoice['id']
        }