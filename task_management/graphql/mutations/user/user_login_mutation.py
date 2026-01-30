from datetime import datetime, timedelta
import graphene
import jwt
from django.conf import settings

from task_management.exceptions import custom_exceptions
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
            access_token = UserLoginMutation._generate_access_token(
                result.user_id)
            return UserType(
                user_id=result.user_id,
                username=result.username,
                email=result.email,
                full_name=result.full_name,
                phone_number=result.phone_number,
                image_url=result.image_url,
                is_active=result.is_active,
                gender=result.gender,
                access_token=access_token
            )

        except custom_exceptions.NotExistedEmailFoundException as e:
            return NotExistedEmailFoundType(email=e.email)

        except custom_exceptions.WrongPasswordFoundException as e:
            return WrongPasswordFoundType(password=e.password)

        except custom_exceptions.InactiveUserException as e:
            return InactiveUserType(user_id=e.user_id)

    @staticmethod
    def _generate_access_token(user_id):
        """Generate JWT access token (no expiry)"""
        payload = {
            'user_id': str(user_id),
            'iat': datetime.utcnow(),
            'type': 'access'
        }
        token = jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm='HS256'
        )
        return token
