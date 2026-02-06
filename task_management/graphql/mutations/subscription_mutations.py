# task_management/graphql/mutations/subscription_mutations.py

import graphene

from task_management.graphql.types.input_types import \
    CreateCheckoutSessionInput, CancelSubscriptionInput
from task_management.graphql.types.subscription_types import (
    CheckoutSessionType,
    SubscriptionType,
    PlanNotFoundType,
    SubscriptionNotFoundType,
    StripeCheckoutErrorType,
    InvalidSubscriptionOwnerType
)
from task_management.interactors.create_checkout_session_interactor import (
    CreateCheckoutSessionInteractor
)
from task_management.interactors.cancel_subscription_interactor import (
    CancelSubscriptionInteractor
)
from task_management.interactors.dtos import CreateCheckoutSessionDTO, CancelSubscriptionDTO
from task_management.storages.plan_storage import PlanStorage
from task_management.storages.customer_storage import CustomerStorage
from task_management.storages.subscription_storage import SubscriptionStorage
from task_management.exceptions.custom_exceptions import (
    PlanNotFoundException,
    SubscriptionNotFoundException,
    StripeCheckoutException,
    InvalidSubscriptionOwnerException
)


# Define Union Types OUTSIDE the mutation class
class CreateCheckoutSessionOutput(graphene.Union):
    class Meta:
        types = (CheckoutSessionType, PlanNotFoundType, StripeCheckoutErrorType)


class CancelSubscriptionOutput(graphene.Union):
    class Meta:
        types = (SubscriptionType, SubscriptionNotFoundType, InvalidSubscriptionOwnerType)


class CreateCheckoutSession(graphene.Mutation):
    class Arguments:
        params = CreateCheckoutSessionInput(required=True)

    # Use the Union type directly as Output
    Output = CreateCheckoutSessionOutput

    @staticmethod
    def mutate(root, info, params):
        user_id = info.context.user_id

        interactor = CreateCheckoutSessionInteractor(
            plan_storage=PlanStorage(),
            customer_storage=CustomerStorage()
        )

        try:
            checkout_dto = CreateCheckoutSessionDTO(
                user_id=str(user_id),
                plan_id=params.plan_id,
                success_url=params.get('success_url'),
                cancel_url=params.get('cancel_url')
            )

            result = interactor.create_checkout_session(checkout_data=checkout_dto)

            return CheckoutSessionType(
                session_id=result.session_id,
                checkout_url=result.checkout_url
            )

        except PlanNotFoundException as e:
            return PlanNotFoundType(plan_id=e.plan_id)

        except StripeCheckoutException as e:
            return StripeCheckoutErrorType(message=e.message)


class CancelSubscription(graphene.Mutation):
    class Arguments:
        params = CancelSubscriptionInput(required=True)

    # Use the Union type directly as Output
    Output = CancelSubscriptionOutput

    @staticmethod
    def mutate(root, info, params):
        user_id = info.context.user_id

        interactor = CancelSubscriptionInteractor(
            subscription_storage=SubscriptionStorage()
        )

        try:
            cancel_dto = CancelSubscriptionDTO(
                user_id=str(user_id),
                subscription_id=params.subscription_id
            )

            result = interactor.cancel_subscription(cancel_data=cancel_dto)

            # Convert DTO to GraphQL type
            from task_management.models import Subscription
            subscription = Subscription.objects.get(subscription_id=result.subscription_id)

            return subscription

        except SubscriptionNotFoundException as e:
            return SubscriptionNotFoundType(subscription_id=e.subscription_id)

        except InvalidSubscriptionOwnerException as e:
            return InvalidSubscriptionOwnerType(
                user_id=e.user_id,
                subscription_id=e.subscription_id
            )


class SubscriptionMutations(graphene.ObjectType):
    create_checkout_session = CreateCheckoutSession.Field()
    cancel_subscription = CancelSubscription.Field()