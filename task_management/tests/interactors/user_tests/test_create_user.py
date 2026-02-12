from unittest.mock import create_autospec
import pytest

from task_management.exceptions.custom_exceptions import (
    UsernameAlreadyExistsException,
    EmailAlreadyExistsException,
    PhoneNumberAlreadyExistsException,
)
from task_management.exceptions.enums import Gender
from task_management.interactors.dtos import CreateUserDTO
from task_management.interactors.storage_interfaces.user_storage_interface import (
    UserStorageInterface,
)
from task_management.interactors.user.user_interactor import (
    UserInteractor,
)


class TestCreateUser:

    def _mock_storage_defaults(self, user_storage):
        user_storage.check_username_exists.return_value = False
        user_storage.check_email_exists.return_value = False
        user_storage.check_phone_number_exists.return_value = False

    def test_create_user_successfully(self, snapshot):
        user_storage = create_autospec(UserStorageInterface)
        self._mock_storage_defaults(user_storage)

        user_storage.create_user.return_value = type(
            "User", (), {"email": "babahajvali@gmail.com"}
        )()

        interactor = UserInteractor(user_storage=user_storage)

        user_input_data = CreateUserDTO(
            full_name="full_name",
            username="Username",
            password="Baba!2#4",
            phone_number="9815267845",
            email="babahajvali@gmail.com",
            gender=Gender.MALE,
            image_url="https://example.com/image.png",
        )

        result = interactor.create_user(user_input_data)

        snapshot.assert_match(
            repr(result.email),
            "test_create_user_successfully.txt",
        )

        user_storage.create_user.assert_called_once_with(
            user_data=user_input_data
        )

    # ---------- USERNAME EXISTS ----------

    def test_create_user_raises_username_exception(self, snapshot):
        user_storage = create_autospec(UserStorageInterface)
        self._mock_storage_defaults(user_storage)

        user_storage.check_username_exists.return_value = True

        interactor = UserInteractor(user_storage=user_storage)

        user_input_data = CreateUserDTO(
            full_name="full_name",
            username="Username",
            password="Baba!2#4",
            phone_number="9815267845",
            email="babahajvali@gmail.com",
            gender=Gender.MALE,
            image_url="https://example.com/image.png",
        )

        with pytest.raises(UsernameAlreadyExistsException) as exc:
            interactor.create_user(user_input_data)

        snapshot.assert_match(
            repr(exc.value.username),
            "test_create_user_raises_username_exception.txt",
        )

    # ---------- EMAIL EXISTS ----------

    def test_create_user_raises_email_exception(self, snapshot):
        user_storage = create_autospec(UserStorageInterface)
        self._mock_storage_defaults(user_storage)

        user_storage.check_email_exists.return_value = True

        interactor = UserInteractor(user_storage=user_storage)

        user_input_data = CreateUserDTO(
            full_name="full_name",
            username="NewUsername1",
            password="Baba!2#4",
            phone_number="9815267845",
            email="existingemail@example.com",
            gender=Gender.MALE,
            image_url="https://example.com/image.png",
        )

        with pytest.raises(EmailAlreadyExistsException) as exc:
            interactor.create_user(user_input_data)

        snapshot.assert_match(
            repr(exc.value),
            "test_create_user_raises_email_exception.txt",
        )

    # ---------- PHONE EXISTS ----------

    def test_create_user_raises_phone_exception(self, snapshot):
        user_storage = create_autospec(UserStorageInterface)
        self._mock_storage_defaults(user_storage)

        user_storage.check_phone_number_exists.return_value = True

        interactor = UserInteractor(user_storage=user_storage)

        user_input_data = CreateUserDTO(
            full_name="full_name",
            username="NewUsername2",
            password="Baba!2#4",
            phone_number="existingphone",
            email="newemail@example.com",
            gender=Gender.MALE,
            image_url="https://example.com/image.png",
        )

        with pytest.raises(PhoneNumberAlreadyExistsException) as exc:
            interactor.create_user(user_input_data)

        snapshot.assert_match(
            repr(exc.value),
            "test_create_user_raises_phone_exception.txt",
        )
