import graphene

from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import UserNotFoundType, \
    InactiveUserType
from task_management.graphql.types.input_types import BlockUserInputParams
from task_management.graphql.types.response_types import BlockUserResponse
from task_management.graphql.types.types import UserType
from task_management.interactors.user_interactor.user_interactors import \
    UserInteractor
from task_management.storages.user_storage import UserStorage


class BlockUserMutation(graphene.Mutation):
    class Arguments:
        params = BlockUserInputParams(required=True)

    Output = BlockUserResponse

    @staticmethod
    def mutate(root, info, params):
        user_storage = UserStorage()
        interactor = UserInteractor(user_storage=user_storage)

        try:
            result = interactor.block_user(user_id=params.user_id)

            return UserType(
                user_id=result.user_id,
                username=result.username,
                email=result.email,
                full_name=result.full_name,
                phone_number=result.phone_number,
                image_url=result.image_url,
                is_active=result.is_active,
                gender=result.gender,
            )

        except custom_exceptions.UserNotFoundException as e:
            return UserNotFoundType(user_id=e.user_id)

        except custom_exceptions.InactiveUserException as e:
            return InactiveUserType(user_id=e.user_id)
