from task_management.graphql.types.types import UserType
from task_management.storages import UserStorage


def get_user_with_email_resolver(root, info, params):
    email = params.email

    user_storage = UserStorage()

    try:
        result = user_storage.get_user_details(email)

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

    except Exception as ex:
        return None
