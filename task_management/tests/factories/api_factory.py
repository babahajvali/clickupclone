import uuid

import factory

from task_management.exceptions.enums import Gender
from task_management.interactors.dtos import UserDTO, AccountDTO


class UserDTOFactory(factory.Factory):
    class Meta:
        model = UserDTO

    user_id = factory.LazyFunction(lambda: str(uuid.uuid4()))
    image_url = factory.Faker("image_url")
    full_name = factory.Faker("name")
    username = factory.Faker("user_name")
    password = "test123"
    email = factory.Faker("email")
    phone_number = factory.Faker("phone_number")
    gender = Gender.MALE.value
    is_active = True


class AccountDTOFactory(factory.Factory):
    class Meta:
        model = AccountDTO

    account_id = factory.LazyFunction(lambda: str(uuid.uuid4()))
    name = factory.Faker("company")
    description = factory.Faker("text")
    owner_id = factory.LazyFunction(lambda: str(uuid.uuid4()))
    is_active = True
