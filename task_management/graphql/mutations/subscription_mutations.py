import graphene

from task_management.exceptions.custom_exceptions import (
    InvalidSubscriptionOwnerException,
    PlanNotFoundException,
    StripeCheckoutException,
    SubscriptionNotFoundException,
)
from task_management.graphql.types.input_types import (
    CancelSubscriptionInput,
    CreateCheckoutSessionInput,
)
from task_management.graphql.types.subscription_types import (
    CheckoutSessionType,
    InvalidSubscriptionOwnerType,
    PlanNotFoundType,
    StripeCheckoutErrorType,
    SubscriptionNotFoundType,
    SubscriptionType,
)
from task_management.interactors.cancel_subscription_interactor import (
    CancelSubscriptionInteractor,
)
from task_management.interactors.create_checkout_session_interactor import (
    CreateCheckoutSessionInteractor,
)
from task_management.interactors.dtos import (
    CancelSubscriptionDTO,
    CreateCheckoutSessionDTO,
)
from task_management.models import Subscription
from task_management.storages.customer_storage import CustomerStorage
from task_management.storages.plan_storage import PlanStorage
from task_management.storages.subscription_storage import SubscriptionStorage


class CreateCheckoutSessionOutput(graphene.Union):
    class Meta:
        types = (CheckoutSessionType, PlanNotFoundType, StripeCheckoutErrorType)


class CancelSubscriptionOutput(graphene.Union):
    class Meta:
        types = (
            SubscriptionType,
            SubscriptionNotFoundType,
            InvalidSubscriptionOwnerType,
        )


class CreateCheckoutSession(graphene.Mutation):
    class Arguments:
        params = CreateCheckoutSessionInput(required=True)

    Output = CreateCheckoutSessionOutput

    @staticmethod
    def mutate(root, info, params):
        interactor = CreateCheckoutSessionInteractor(
            plan_storage=PlanStorage(),
            customer_storage=CustomerStorage(),
        )
        try:
            result = interactor.create_checkout_session(
                checkout_data=CreateCheckoutSessionDTO(
                    user_id=str(info.context.user_id),
                    plan_id=params.plan_id,
                    success_url=getattr(params, "success_url", None),
                    cancel_url=getattr(params, "cancel_url", None),
                )
            )
        except PlanNotFoundException as exc:
            return PlanNotFoundType(plan_id=exc.plan_id)
        except StripeCheckoutException as exc:
            return StripeCheckoutErrorType(message=exc.message)

        return CheckoutSessionType(
            session_id=result.session_id,
            checkout_url=result.checkout_url,
        )


class CancelSubscription(graphene.Mutation):
    class Arguments:
        params = CancelSubscriptionInput(required=True)

    Output = CancelSubscriptionOutput

    @staticmethod
    def mutate(root, info, params):
        interactor = CancelSubscriptionInteractor(
            subscription_storage=SubscriptionStorage()
        )
        try:
            result = interactor.cancel_subscription(
                cancel_data=CancelSubscriptionDTO(
                    user_id=str(info.context.user_id),
                    subscription_id=params.subscription_id,
                )
            )
        except SubscriptionNotFoundException as exc:
            return SubscriptionNotFoundType(subscription_id=exc.subscription_id)
        except InvalidSubscriptionOwnerException as exc:
            return InvalidSubscriptionOwnerType(
                user_id=exc.user_id,
                subscription_id=exc.subscription_id,
            )

        return Subscription.objects.get(subscription_id=result.subscription_id)


class SubscriptionMutations(graphene.ObjectType):
    create_checkout_session = CreateCheckoutSession.Field()
    cancel_subscription = CancelSubscription.Field()
