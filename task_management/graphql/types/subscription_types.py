import graphene
from graphene_django import DjangoObjectType

from task_management.models import Payment, Plan, Subscription


class PlanType(DjangoObjectType):
    class Meta:
        model = Plan
        fields = (
            "plan_id",
            "plan_name",
            "stripe_price_id",
            "price",
            "currency",
            "billing_period",
            "features",
            "is_active",
        )


class SubscriptionType(DjangoObjectType):
    class Meta:
        model = Subscription
        fields = (
            "subscription_id",
            "user",
            "plan",
            "stripe_subscription_id",
            "status",
            "current_period_start",
            "current_period_end",
            "cancel_at_period_end",
            "canceled_at",
        )


class PaymentType(DjangoObjectType):
    class Meta:
        model = Payment
        fields = (
            "payment_id",
            "user",
            "subscription",
            "stripe_payment_intent_id",
            "amount",
            "currency",
            "status",
            "payment_method",
            "created_at",
        )


class CheckoutSessionType(graphene.ObjectType):
    session_id = graphene.String(required=True)
    checkout_url = graphene.String(required=True)


class PlanNotFoundType(graphene.ObjectType):
    plan_id = graphene.String(required=True)


class SubscriptionNotFoundType(graphene.ObjectType):
    subscription_id = graphene.String(required=True)


class StripeCheckoutErrorType(graphene.ObjectType):
    message = graphene.String(required=True)


class InvalidSubscriptionOwnerType(graphene.ObjectType):
    user_id = graphene.String(required=True)
    subscription_id = graphene.String(required=True)
