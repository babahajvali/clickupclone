# task_management/graphql/queries/subscription_queries.py

import graphene
from typing import List
from task_management.graphql.types.subscription_types import (
    PlanType,
    SubscriptionType,
    PaymentType
)
from task_management.interactors.get_plans_interactor import GetPlansInteractor
from task_management.interactors.get_subscription_details_interactor import (
    GetSubscriptionDetailsInteractor
)
from task_management.interactors.get_payment_history_interactor import (
    GetPaymentHistoryInteractor
)
from task_management.storages.plan_storage import PlanStorage
from task_management.storages.subscription_storage import SubscriptionStorage
from task_management.storages.payment_storage import PaymentStorage
from task_management.models import Plan, Subscription, Payment


class SubscriptionQueries(graphene.ObjectType):
    get_available_plans = graphene.List(PlanType)
    get_my_subscription = graphene.Field(SubscriptionType)
    get_my_payments = graphene.List(PaymentType)

    @staticmethod
    def resolve_get_available_plans(root, info):
        """Get all available subscription plans"""
        interactor = GetPlansInteractor(plan_storage=PlanStorage())
        plans_dto = interactor.get_all_plans()

        # Convert DTOs to Django models for GraphQL
        plan_ids = [plan.plan_id for plan in plans_dto]
        return Plan.objects.filter(plan_id__in=plan_ids, is_active=True)

    @staticmethod
    def resolve_get_my_subscription(root, info):
        """Get current user's active subscription"""
        user_id = info.context.user.pk

        interactor = GetSubscriptionDetailsInteractor(
            subscription_storage=SubscriptionStorage()
        )

        subscription_dto = interactor.get_user_subscription(user_id=str(user_id))

        if not subscription_dto:
            return None

        # Return Django model instance
        return Subscription.objects.get(subscription_id=subscription_dto.subscription_id)

    @staticmethod
    def resolve_get_my_payments(root, info):
        """Get current user's payment history"""
        user_id = info.context.user_id

        interactor = GetPaymentHistoryInteractor(
            payment_storage=PaymentStorage()
        )

        payments_dto = interactor.get_user_payments(user_id=str(user_id))

        # Convert DTOs to Django models
        payment_ids = [payment.payment_id for payment in payments_dto]
        return Payment.objects.filter(payment_id__in=payment_ids)