import pytest

from task_management.exceptions.enums import Role
from task_management.interactors.dtos import CreateAccountMemberDTO
from task_management.storages.account_member_storage import AccountMemberStorage
from task_management.tests.factories.storage_factory import AccountMemberFactory, UserFactory, AccountFactory


class TestAccountMemberStorage:

    @pytest.mark.django_db
    def test_get_user_permission_for_account_success(self, snapshot):
        # Arrange - use fixed UUIDs
        account_id = "12345678-1234-5678-1234-567812345678"
        user_id = "12345678-1234-5678-1234-567812345679"
        added_by_id = "12345678-1234-5678-1234-567812345680"  # Fixed UUID

        user = UserFactory(user_id=user_id)
        account = AccountFactory(account_id=account_id)
        added_by = UserFactory(user_id=added_by_id)  # Use fixed UUID
        AccountMemberFactory(account=account, user=user, added_by=added_by,
                             role="member")
        storage = AccountMemberStorage()

        # Act
        result = storage.get_user_permission_for_account(
            account_id=str(account_id), user_id=str(user_id))

        # Assert
        snapshot.assert_match(repr(result),
                              "test_get_user_permission_for_account_success.txt")

    @pytest.mark.django_db
    def test_get_user_permission_for_account_failure(self, snapshot):
        # Arrange
        account_id = "12345678-1234-5678-1234-567812345678"
        user_id = "12345678-1234-5678-1234-567812345679"
        storage = AccountMemberStorage()

        # Act
        result = storage.get_user_permission_for_account(account_id=str(account_id), user_id=str(user_id))

        # Assert
        snapshot.assert_match(repr(result), "test_get_user_permission_for_account_failure.txt")

    @pytest.mark.django_db
    def test_add_member_to_account_success(self, snapshot):
        # Arrange
        account_id = "12345678-1234-5678-1234-567812345678"
        user_id = "12345678-1234-5678-1234-567812345679"
        added_by_id = "12345678-1234-5678-1234-567812345680"
        user = UserFactory(user_id=user_id)
        added_by = UserFactory(user_id=added_by_id)
        account = AccountFactory(account_id=account_id)
        user_data = CreateAccountMemberDTO(
            account_id=str(account_id),
            user_id=str(user_id),
            added_by=str(added_by_id),
            role=Role.MEMBER
        )
        storage = AccountMemberStorage()

        # Act
        result = storage.add_member_to_account(user_data=user_data)

        # Assert
        snapshot.assert_match(repr(result), "test_add_member_to_account_success.txt")

    @pytest.mark.django_db
    def test_update_member_role_success(self, snapshot):
        # Arrange
        user = UserFactory(user_id="12345678-1234-5678-1234-567812345681")
        account = AccountFactory(
            account_id="12345678-1234-5678-1234-567812345682")
        added_by = UserFactory(user_id="12345678-1234-5678-1234-567812345683")
        account_member = AccountMemberFactory(account=account, user=user,
                                              added_by=added_by, role="member")
        storage = AccountMemberStorage()

        # Act
        result = storage.update_member_role(
            account_member_id=account_member.pk, role=Role.ADMIN)

        # Assert
        snapshot.assert_match(repr(result),
                              "test_update_member_role_success.txt")

    @pytest.mark.django_db
    def test_get_account_member_permission_success(self, snapshot):
        # Arrange
        user_id = "12345678-1234-5678-1234-567812345684"
        account_id = "12345678-1234-5678-1234-567812345685"
        added_by_id = "12345678-1234-5678-1234-567812345686"

        user = UserFactory(user_id=user_id)
        account = AccountFactory(account_id=account_id)
        added_by = UserFactory(user_id=added_by_id)
        account_member = AccountMemberFactory(account=account, user=user,
                                              added_by=added_by, role="admin")
        storage = AccountMemberStorage()

        # Act
        result = storage.get_account_member_permission(
            account_member_id=account_member.pk)

        # Assert
        snapshot.assert_match(repr(result),
                              "test_get_account_member_permission_success.txt")

    @pytest.mark.django_db
    def test_delete_account_member_permission_success(self, snapshot):
        # Arrange
        user_id = "12345678-1234-5678-1234-567812345687"
        account_id = "12345678-1234-5678-1234-567812345688"
        added_by_id = "12345678-1234-5678-1234-567812345689"

        user = UserFactory(user_id=user_id)
        account = AccountFactory(account_id=account_id)
        added_by = UserFactory(user_id=added_by_id)
        account_member = AccountMemberFactory(account=account, user=user,
                                              added_by=added_by,
                                              is_active=True)
        storage = AccountMemberStorage()

        # Act
        result = storage.delete_account_member_permission(
            account_member_id=account_member.pk)

        # Assert
        snapshot.assert_match(repr(result),
                              "test_delete_account_member_permission_success.txt")