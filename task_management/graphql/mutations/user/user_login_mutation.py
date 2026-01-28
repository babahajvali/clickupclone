import graphene

from task_management.exceptions import custom_exceptions
from task_management.exceptions.custom_exceptions import InactiveUserException
from task_management.graphql.types.error_types import NotExistedEmailFoundType, \
    WrongPasswordFoundType, InactiveUserType
from task_management.graphql.types.input_types import UserLoginInputParams
from task_management.graphql.types.response_types import UserLoginResponse
from task_management.graphql.types.types import UserType
from task_management.interactors.user_interactor.user_interactors import \
    UserInteractor
from task_management.storages.user_storage import UserStorage


class UserLoginMutation(graphene.Mutation):
    class Arguments:
        params = UserLoginInputParams(required=True)

    Output = UserLoginResponse

    @staticmethod
    def mutate(root, info, params):
        user_storage = UserStorage()
        interactor = UserInteractor(user_storage=user_storage)

        try:
            result = interactor.user_login(
                email=params.email,
                password=params.password
            )

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

        except custom_exceptions.NotExistedEmailFoundException as e:
            return NotExistedEmailFoundType(email=e.email)

        except custom_exceptions.WrongPasswordFoundException as e:
            return WrongPasswordFoundType(password=e.password)

        except custom_exceptions.InactiveUserException as e:
            return InactiveUserType(user_id=e.user_id)
