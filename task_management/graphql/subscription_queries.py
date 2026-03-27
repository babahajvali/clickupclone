import graphene

from task_management.graphql.types.subscription_types import (
    PaymentType,
    PlanType,
    SubscriptionType,
)
from task_management.interactors.get_payment_history_interactor import (
    GetPaymentHistoryInteractor,
)
from task_management.interactors.get_plans_interactor import GetPlansInteractor
from task_management.interactors.get_subscription_details_interactor import (
    GetSubscriptionDetailsInteractor,
)
from task_management.models import Payment, Plan, Subscription
from task_management.storages.payment_storage import PaymentStorage
from task_management.storages.plan_storage import PlanStorage
from task_management.storages.subscription_storage import SubscriptionStorage


class SubscriptionQueries(graphene.ObjectType):
    get_available_plans = graphene.List(PlanType)
    get_my_subscription = graphene.Field(SubscriptionType)
    get_my_payments = graphene.List(PaymentType)

    @staticmethod
    def resolve_get_available_plans(root, info):
        interactor = GetPlansInteractor(plan_storage=PlanStorage())
        plan_ids = [plan.plan_id for plan in interactor.get_all_plans()]
        return Plan.objects.filter(plan_id__in=plan_ids, is_active=True)

    @staticmethod
    def resolve_get_my_subscription(root, info):
        user_id = info.context.user_id
        interactor = GetSubscriptionDetailsInteractor(
            subscription_storage=SubscriptionStorage()
        )
        subscription_dto = interactor.get_user_subscription(user_id=str(user_id))
        if subscription_dto is None:
            return None
        return Subscription.objects.get(subscription_id=subscription_dto.subscription_id)

    @staticmethod
    def resolve_get_my_payments(root, info):
        user_id = info.context.user_id
        interactor = GetPaymentHistoryInteractor(payment_storage=PaymentStorage())
        payment_ids = [payment.payment_id for payment in interactor.get_user_payments(user_id=str(user_id))]
        return Payment.objects.filter(payment_id__in=payment_ids)
