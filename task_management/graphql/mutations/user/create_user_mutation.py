import graphene

from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import ExistedUsernameFoundType, \
    ExistedEmailFoundType, ExistedPhoneNumberFoundType
from task_management.graphql.types.input_types import CreateUserInputParams
from task_management.graphql.types.response_types import CreateUserResponse
from task_management.graphql.types.types import UserType
from task_management.interactors.dtos import CreateUserDTO
from task_management.interactors.user_interactor.user_interactors import \
    UserInteractor
from task_management.storages.user_storage import UserStorage


class CreateUserMutation(graphene.Mutation):
    class Arguments:
        params = CreateUserInputParams(required=True)

    Output = CreateUserResponse

    @staticmethod
    def mutate(root, info, params):
        user_storage = UserStorage()
        interactor = UserInteractor(user_storage=user_storage)

        try:
            user_input_data = CreateUserDTO(
                username=params.username,
                email=params.email,
                password=params.password,
                full_name=params.full_name,
                phone_number=params.phone_number,
                gender=params.gender,
                image_url=params.image_url,
            )

            result = interactor.create_user(user_details=user_input_data)

            return UserType(
                user_id=result.user_id,
                username=result.username,
                email=result.email,
                full_name=result.full_name,
                phone_number=result.phone_number,
                image_url=result.image_url,
                is_active=result.is_active,
                gender=result.gender
            )

        except custom_exceptions.ExistedUsernameFoundException as e:
            return ExistedUsernameFoundType(username=e.username)

        except custom_exceptions.ExistedEmailFoundException as e:
            return ExistedEmailFoundType(email=e.email)
        except custom_exceptions.ExistedPhoneNumberFoundException as e:
            return ExistedPhoneNumberFoundType(phone_number=e.phone_number)
