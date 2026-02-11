import pytest

from task_management.interactors.dtos import CreateAccountDTO
from task_management.storages.account_storage import AccountStorage
from task_management.tests.factories.storage_factory import AccountFactory, UserFactory


class TestAccountStorage:

    @pytest.mark.django_db
    def test_get_account_by_id_success(self, snapshot):
        # Arrange
        account_id = "12345678-1234-5678-1234-567812345678"
        owner_id = "12345678-1234-5678-1234-567812345690"
        owner = UserFactory(user_id=owner_id)
        AccountFactory(
            account_id=account_id,
            name="Test Account",
            description="Test account description",  # Fixed description
            owner=owner
        )
        storage = AccountStorage()

        # Act
        result = storage.get_account_by_id(account_id=str(account_id))

        # Assert
        snapshot.assert_match(repr(result), "test_get_account_by_id_success.txt")

    @pytest.mark.django_db
    def test_get_account_by_id_failure(self, snapshot):
        # Arrange
        account_id = "12345678-1234-5678-1234-567812345678"
        storage = AccountStorage()

        # Act
        result = storage.get_account_by_id(account_id=str(account_id))

        # Assert
        snapshot.assert_match(repr(result), "test_get_account_by_id_failure.txt")

    @pytest.mark.django_db
    def test_validate_account_name_exists_success(self, snapshot):
        # Arrange
        name = "Existing Account"
        owner_id = "12345678-1234-5678-1234-567812345691"
        owner = UserFactory(user_id=owner_id)
        AccountFactory(name=name, owner=owner)
        storage = AccountStorage()

        # Act
        result = storage.validate_account_name_exists(name=name)

        # Assert
        snapshot.assert_match(repr(result), "test_validate_account_name_exists_success.txt")

    @pytest.mark.django_db
    def test_validate_account_name_exists_failure(self, snapshot):
        # Arrange
        name = "Non Existing Account"
        storage = AccountStorage()

        # Act
        result = storage.validate_account_name_exists(name=name)

        # Assert
        snapshot.assert_match(repr(result), "test_validate_account_name_exists_failure.txt")

    @pytest.mark.django_db
    def test_create_account_success(self):  # No snapshot, no mock
        # Arrange
        owner_id = "12345678-1234-5678-1234-567812345678"
        owner = UserFactory(user_id=owner_id)
        account_dto = CreateAccountDTO(
            name="New Account",
            description="New account description",
            owner_id=str(owner_id)
        )
        storage = AccountStorage()

        # Act
        result = storage.create_account(account_dto=account_dto)

        # Assert - Test what matters
        assert result.name == "New Account"
        assert result.description == "New account description"
        assert str(result.owner_id) == owner_id

    @pytest.mark.django_db
    def test_transfer_account_success(self, snapshot):
        # Arrange
        account_id = "12345678-1234-5678-1234-567812345678"
        old_owner_id = "12345678-1234-5678-1234-567812345679"
        new_owner_id = "12345678-1234-5678-1234-567812345680"
        old_owner = UserFactory(user_id=old_owner_id)
        new_owner = UserFactory(user_id=new_owner_id)
        AccountFactory(
            account_id=account_id,
            name="Transfer Account",  # Fixed name
            description="Transfer account description",  # Fixed description
            owner=old_owner
        )
        storage = AccountStorage()

        # Act
        result = storage.transfer_account(account_id=str(account_id), new_owner_id=str(new_owner_id))

        # Assert
        snapshot.assert_match(repr(result), "test_transfer_account_success.txt")

    @pytest.mark.django_db
    def test_delete_account_success(self, snapshot):
        # Arrange
        account_id = "12345678-1234-5678-1234-567812345678"
        owner_id = "12345678-1234-5678-1234-567812345692"
        owner = UserFactory(user_id=owner_id)
        AccountFactory(
            account_id=account_id,
            name="Delete Account",  # Fixed name
            description="Delete account description",  # Fixed description
            owner=owner,
            is_active=True
        )
        storage = AccountStorage()

        # Act
        result = storage.deactivate_account(account_id=str(account_id))

        # Assert
        snapshot.assert_match(repr(result), "test_delete_account_success.txt")