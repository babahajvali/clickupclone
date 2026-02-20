import pytest

from task_management.storages.account_storage import AccountStorage
from task_management.tests.factories.storage_factory import AccountFactory, \
    UserFactory


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
            description="Test accounts description",  # Fixed description
            owner=owner
        )
        storage = AccountStorage()

        # Act
        result = storage.get_account_by_id(account_id=str(account_id))

        # Assert
        snapshot.assert_match(repr(result),
                              "test_get_account_by_id_success.txt")

    @pytest.mark.django_db
    def test_get_account_by_id_failure(self, snapshot):
        # Arrange
        account_id = "12345678-1234-5678-1234-567812345678"
        storage = AccountStorage()

        # Act
        result = storage.get_account_by_id(account_id=str(account_id))

        # Assert
        snapshot.assert_match(repr(result),
                              "test_get_account_by_id_failure.txt")

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
        snapshot.assert_match(repr(result),
                              "test_validate_account_name_exists_success.txt")

    @pytest.mark.django_db
    def test_validate_account_name_exists_failure(self, snapshot):
        # Arrange
        name = "Non Existing Account"
        storage = AccountStorage()

        # Act
        result = storage.validate_account_name_exists(name=name)

        # Assert
        snapshot.assert_match(repr(result),
                              "test_validate_account_name_exists_failure.txt")

    @pytest.mark.django_db
    def test_create_account_success(self):  # No snapshot, no mock
        # Arrange
        owner_id = "12345678-1234-5678-1234-567812345678"
        owner = UserFactory(user_id=owner_id)
        name = "New Account"
        description = "New accounts description"
        owner_id = str(owner_id)

        storage = AccountStorage()

        # Act
        result = storage.create_account(name=name, description=description,
                                        created_by=owner_id)

        # Assert - Test what matters
        assert result.name == "New Account"
        assert result.description == "New accounts description"
        assert str(result.owner_id) == owner_id

    @pytest.mark.django_db
    def test_delete_account_success(self, snapshot):
        # Arrange
        account_id = "12345678-1234-5678-1234-567812345678"
        owner_id = "12345678-1234-5678-1234-567812345692"
        owner = UserFactory(user_id=owner_id)
        AccountFactory(
            account_id=account_id,
            name="Delete Account",  # Fixed name
            description="Delete accounts description",  # Fixed description
            owner=owner,
            is_active=True
        )
        storage = AccountStorage()

        # Act
        result = storage.deactivate_account(account_id=str(account_id))

        # Assert
        snapshot.assert_match(repr(result), "test_delete_account_success.txt")
