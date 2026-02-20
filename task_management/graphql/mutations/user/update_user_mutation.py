import graphene

from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import UsernameAlreadyExists, \
    EmailAlreadyExists, PhoneNumberAlreadyExists, UserNotFoundType
from task_management.graphql.types.input_types import UpdateUserInputParams
from task_management.graphql.types.response_types import UpdateUserResponse
from task_management.graphql.types.types import UserType
from task_management.interactors.dtos import UpdateUserDTO
from task_management.interactors.user.user_interactor import \
    UserInteractor
from task_management.storages import UserStorage


class UpdateUserMutation(graphene.Mutation):
    class Arguments:
        params = UpdateUserInputParams(required=True)

    Output = UpdateUserResponse

    @staticmethod
    def mutate(root, info, params):
        user_storage = UserStorage()
        interactor = UserInteractor(user_storage=user_storage)

        try:
            user_update_data = UpdateUserDTO(
                user_id=info.context.user_id,
                username=params.username if params.username else None,
                email=params.email if params.email else None,
                full_name=params.full_name if params.full_name else None,
                phone_number=params.phone_number if params.phone_number else None,
                gender=params.gender if params.gender else None,
                image_url=params.image_url if params.image_url else None,
            )

            result = interactor.update_user(user_update_data=user_update_data)

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

        except custom_exceptions.UserNotFound as e:
            return UserNotFoundType(user_id=e.user_id)

        except custom_exceptions.UsernameAlreadyExists as e:
            return UsernameAlreadyExists(username=e.username)

        except custom_exceptions.EmailAlreadyExists as e:
            return EmailAlreadyExists(email=e.email)

        except custom_exceptions.PhoneNumberAlreadyExists as e:
            return PhoneNumberAlreadyExists(phone_number=e.phone_number)
