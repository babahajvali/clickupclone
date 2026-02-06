# task_management/graphql/types/subscription_types.py

import graphene
from graphene_django import DjangoObjectType
from task_management.models import Plan, Subscription, Payment


class PlanType(DjangoObjectType):
    class Meta:
        model = Plan
        fields = ('plan_id', 'plan_name', 'stripe_price_id', 'price',
                  'currency', 'billing_period', 'features', 'is_active')


class SubscriptionType(DjangoObjectType):
    plan_id = graphene.String()

    class Meta:
        model = Subscription
        fields = ('subscription_id', 'user', 'plan', 'stripe_subscription_id',
                  'status', 'current_period_start', 'current_period_end',
                  'cancel_at_period_end', 'canceled_at', 'created_at')

    def resolve_plan_id(self, info):
        return str(self.plan.plan_id) if self.plan else None


class PaymentType(DjangoObjectType):
    class Meta:
        model = Payment
        fields = ('payment_id', 'user', 'subscription',
                  'stripe_payment_intent_id',
                  'amount', 'currency', 'status', 'payment_method',
                  'created_at')


# Success response types
class CheckoutSessionType(graphene.ObjectType):
    session_id = graphene.String(required=True)
    checkout_url = graphene.String(required=True)


# Error response types
class PlanNotFoundType(graphene.ObjectType):
    plan_id = graphene.String(required=True)


class SubscriptionNotFoundType(graphene.ObjectType):
    subscription_id = graphene.String(required=True)


class StripeCheckoutErrorType(graphene.ObjectType):
    message = graphene.String(required=True)


class InvalidSubscriptionOwnerType(graphene.ObjectType):
    user_id = graphene.String(required=True)
    subscription_id = graphene.String(required=True)