from task_management.exceptions import custom_exceptions
from task_management.interactors.user.user_interactor import UserInteractor
from task_management.graphql.types.error_types import UserNotFoundType, InactiveUserType
from task_management.graphql.types.types import UserType
from task_management.storages import UserStorage


def get_user_profile_resolver(root, info, params):
    user_id = params.user_id

    user_storage = UserStorage()
    interactor = UserInteractor(user_storage=user_storage)

    try:
        user_data = interactor.get_user_profile(user_id=user_id)

        user_output = UserType(
            user_id=user_data.user_id,
            username=user_data.username,
            email=user_data.email,
            full_name=user_data.full_name,
            phone_number=user_data.phone_number,
            image_url=user_data.image_url,
            is_active=user_data.is_active,
            gender=user_data.gender,
        )

        return user_output

    except custom_exceptions.UserNotFound as e:
        return UserNotFoundType(user_id=e.user_id)

    except custom_exceptions.InactiveUser as e:
        return InactiveUserType(user_id=e.user_id)