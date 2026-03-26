from datetime import timedelta

import pytest
from django.utils import timezone

from task_management.exceptions.enums import Gender
from task_management.interactors.dtos import CreateUserDTO, UpdateUserDTO
from task_management.models import PasswordResetToken
from task_management.storages.user_storage import UserStorage
from task_management.tests.factories.storage_factory import UserFactory


class TestUserStorage:

    @pytest.mark.django_db
    def test_get_user_success(self):
        user_id = "12345678-1234-5678-1234-567812345678"
        user = UserFactory(
            user_id=user_id,
            username="reviewer",
            full_name="Code Reviewer",
            email="reviewer@example.com",
            phone_number="+15550000001",
            image_url="https://example.com/reviewer.png",
            gender=Gender.MALE.value,
            is_active=True,
        )
        storage = UserStorage()

        result = storage.get_user(user_id=str(user.user_id))

        assert str(result.user_id) == user_id
        assert result.username == "reviewer"
        assert result.full_name == "Code Reviewer"
        assert result.email == "reviewer@example.com"
        assert result.phone_number == "+15550000001"
        assert result.image_url == "https://example.com/reviewer.png"
        assert result.gender == Gender.MALE.value
        assert result.is_active is True

    @pytest.mark.django_db
    def test_get_user_returns_none_when_missing(self):
        storage = UserStorage()

        result = storage.get_user(
            user_id="12345678-1234-5678-1234-567812345678"
        )

        assert result is None

    @pytest.mark.django_db
    def test_get_user_by_email_success(self):
        user = UserFactory(
            email="lookup@example.com",
            username="lookup_user",
            phone_number="+15550000002",
        )
        storage = UserStorage()

        result = storage.get_user_by_email(email="lookup@example.com")

        assert str(result.user_id) == str(user.user_id)
        assert result.username == "lookup_user"
        assert result.email == "lookup@example.com"

    @pytest.mark.django_db
    def test_get_user_by_email_returns_none_when_missing(self):
        storage = UserStorage()

        result = storage.get_user_by_email(email="missing@example.com")

        assert result is None

    @pytest.mark.django_db
    def test_create_user_returns_dto_with_stored_password(self):
        storage = UserStorage()
        user_data = CreateUserDTO(
            username="new_user",
            full_name="New User",
            email="new@example.com",
            password="secret123",
            phone_number="+15550000003",
            gender=Gender.FEMALE,
            image_url="https://example.com/new.png",
        )

        result = storage.create_user(create_user_dto=user_data)

        assert result.username == "new_user"
        assert result.full_name == "New User"
        assert result.email == "new@example.com"
        assert result.phone_number == "+15550000003"
        assert result.gender == Gender.FEMALE.value
        assert result.image_url == "https://example.com/new.png"
        assert result.password == "secret123"

    @pytest.mark.django_db
    def test_update_user_updates_only_provided_fields(self):
        user = UserFactory(
            username="before_update",
            full_name="Before Update",
            email="before@example.com",
            phone_number="+15550000004",
            image_url="https://example.com/before.png",
            gender=Gender.MALE.value,
        )
        storage = UserStorage()
        update_data = UpdateUserDTO(
            user_id=str(user.user_id),
            full_name="After Update",
            username="after_update",
            gender=Gender.OTHER,
            email="after@example.com",
            phone_number="+15550000005",
            image_url="https://example.com/after.png",
        )

        result = storage.update_user(update_user_dto=update_data)

        assert result.username == "after_update"
        assert result.full_name == "After Update"
        assert result.email == "after@example.com"
        assert result.phone_number == "+15550000005"
        assert result.image_url == "https://example.com/after.png"
        assert result.gender == Gender.OTHER.value

    @pytest.mark.django_db
    def test_block_user_marks_user_inactive(self):
        user = UserFactory(is_active=True)
        storage = UserStorage()

        result = storage.block_user(user_id=str(user.user_id))

        assert result.is_active is False

    @pytest.mark.django_db
    def test_uniqueness_checks(self):
        user = UserFactory(
            username="taken_user",
            email="taken@example.com",
            phone_number="+15550000006",
        )
        storage = UserStorage()

        assert storage.check_username_exists(username="taken_user") is True
        assert storage.check_email_exists(email="taken@example.com") is True
        assert storage.check_phone_number_exists(
            phone_number="+15550000006"
        ) is True
        assert storage.check_user_exists(user_id=str(user.user_id)) is True
        assert storage.check_username_exists(username="free_user") is False
        assert storage.check_email_exists(email="free@example.com") is False
        assert storage.check_phone_number_exists(
            phone_number="+15550000007"
        ) is False

    @pytest.mark.django_db
    def test_uniqueness_checks_excluding_current_user(self):
        current_user = UserFactory(
            username="current_user",
            email="current@example.com",
            phone_number="+15550000008",
        )
        UserFactory(
            username="other_user",
            email="other@example.com",
            phone_number="+15550000009",
        )
        storage = UserStorage()

        assert storage.check_username_except_current_user(
            user_id=str(current_user.user_id),
            username="current_user",
        ) is False
        assert storage.check_email_exists_except_current_user(
            user_id=str(current_user.user_id),
            email="current@example.com",
        ) is False
        assert storage.check_phone_number_except_current_user(
            user_id=str(current_user.user_id),
            phone_number="+15550000008",
        ) is False

        assert storage.check_username_except_current_user(
            user_id=str(current_user.user_id),
            username="other_user",
        ) is True
        assert storage.check_email_exists_except_current_user(
            user_id=str(current_user.user_id),
            email="other@example.com",
        ) is True
        assert storage.check_phone_number_except_current_user(
            user_id=str(current_user.user_id),
            phone_number="+15550000009",
        ) is True

    @pytest.mark.django_db
    def test_create_password_reset_token_replaces_existing_unused_token(self):
        user = UserFactory()
        PasswordResetToken.objects.create(
            user=user,
            token="old-token",
            expires_at=timezone.now() + timedelta(hours=1),
            is_used=False,
        )
        storage = UserStorage()
        expires_at = timezone.now() + timedelta(hours=2)

        result = storage.create_password_reset_token(
            user_id=str(user.user_id),
            token="new-token",
            expires_at=expires_at,
        )

        assert result.user_id == str(user.user_id)
        assert result.token == "new-token"
        assert result.is_used is False

    @pytest.mark.django_db
    def test_get_reset_token_returns_dto_when_found(self):
        user = UserFactory()
        expires_at = timezone.now() + timedelta(hours=1)
        PasswordResetToken.objects.create(
            user=user,
            token="lookup-token",
            expires_at=expires_at,
            is_used=False,
        )
        storage = UserStorage()

        result = storage.get_reset_token(token="lookup-token")

        assert result is not None
        assert result.user_id == str(user.user_id)
        assert result.token == "lookup-token"
        assert result.is_used is False
        assert result.expires_at == expires_at

    @pytest.mark.django_db
    def test_get_reset_token_returns_none_when_missing(self):
        storage = UserStorage()

        result = storage.get_reset_token(token="missing-token")

        assert result is None

    @pytest.mark.django_db
    def test_used_reset_token_marks_token_as_used(self):
        user = UserFactory()
        PasswordResetToken.objects.create(
            user=user,
            token="used-token",
            expires_at=timezone.now() + timedelta(hours=1),
            is_used=False,
        )
        storage = UserStorage()

        result = storage.used_reset_token(token="used-token")

        assert result is True

    @pytest.mark.django_db
    def test_update_user_password_returns_updated_password(self):
        user = UserFactory(password="old-password")
        storage = UserStorage()

        result = storage.update_user_password(
            user_id=str(user.user_id),
            new_password="new-password-123",
        )

        assert str(result.user_id) == str(user.user_id)
        assert result.password == "new-password-123"
