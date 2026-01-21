import pytest

from task_management.interactors.dtos import (
    CreateWorkspaceDTO,
    UpdateWorkspaceDTO
)
from task_management.storages.workspace_storage import WorkspaceStorage
from task_management.tests.factories.storage_factory import (
    WorkspaceFactory,
    UserFactory,
    AccountFactory
)


class TestWorkspaceStorage:

    @pytest.mark.django_db
    def test_get_workspace_success(self, snapshot):
        # Arrange
        workspace_id = "12345678-1234-5678-1234-567812345678"
        user = UserFactory()
        account = AccountFactory(owner=user)
        workspace = WorkspaceFactory(
            workspace_id=workspace_id,
            created_by=user,
            account=account
        )
        storage = WorkspaceStorage()

        # Act
        result = storage.get_workspace(workspace_id=str(workspace_id))

        # Assert
        snapshot.assert_match(
            repr(result),
            "test_get_workspace_success.txt"
        )

    @pytest.mark.django_db
    def test_get_workspace_failure(self, snapshot):
        # Arrange
        storage = WorkspaceStorage()

        # Act
        result = storage.get_workspace(
            workspace_id="12345678-1234-5678-1234-567812345612"
        )

        # Assert
        snapshot.assert_match(
            repr(result),
            "test_get_workspace_failure.txt"
        )

    @pytest.mark.django_db
    def test_create_workspace(self, snapshot):
        # Arrange
        user_id = "12345678-1234-5678-1234-567812345679"
        account_id = "12345678-1234-5678-1234-567812345680"

        user = UserFactory(user_id=user_id)
        account = AccountFactory(account_id=account_id, owner=user)

        dto = CreateWorkspaceDTO(
            name="My Workspace",
            description="Workspace description",
            user_id=str(user_id),
            account_id=str(account_id)
        )
        storage = WorkspaceStorage()

        # Act
        result = storage.create_workspace(workspace_data=dto)

        # Assert
        snapshot.assert_match(
            repr(result),
            "test_create_workspace.txt"
        )

    @pytest.mark.django_db
    def test_update_workspace(self, snapshot):
        # Arrange
        workspace_id = "12345678-1234-5678-1234-567812345678"
        user = UserFactory()
        account = AccountFactory(owner=user)
        workspace = WorkspaceFactory(
            workspace_id=workspace_id,
            created_by=user,
            account=account
        )

        dto = UpdateWorkspaceDTO(
            workspace_id=str(workspace_id),
            name="Updated Workspace",
            description="Updated description"
        )
        storage = WorkspaceStorage()

        # Act
        result = storage.update_workspace(workspace_data=dto)

        # Assert
        snapshot.assert_match(
            repr(result),
            "test_update_workspace.txt"
        )

    @pytest.mark.django_db
    def test_delete_workspace(self, snapshot):
        # Arrange
        workspace_id = "12345678-1234-5678-1234-567812345678"
        user = UserFactory()
        account = AccountFactory(owner=user)
        workspace = WorkspaceFactory(
            workspace_id=workspace_id,
            created_by=user,
            account=account,
            is_active=True
        )
        storage = WorkspaceStorage()

        # Act
        result = storage.delete_workspace(
            workspace_id=str(workspace_id)
        )

        # Assert
        snapshot.assert_match(
            repr(result),
            "test_delete_workspace.txt"
        )

    @pytest.mark.django_db
    def test_transfer_workspace(self, snapshot):
        # Arrange
        workspace_id = "12345678-1234-5678-1234-567812345678"
        old_owner = UserFactory()
        new_owner = UserFactory()
        account = AccountFactory(owner=old_owner)

        workspace = WorkspaceFactory(
            workspace_id=workspace_id,
            created_by=old_owner,
            account=account
        )
        storage = WorkspaceStorage()

        # Act
        result = storage.transfer_workspace(
            workspace_id=str(workspace_id),
            new_user_id=str(new_owner.user_id)
        )

        # Assert
        snapshot.assert_match(
            repr(result),
            "test_transfer_workspace.txt"
        )

    @pytest.mark.django_db
    def test_get_workspaces_by_account(self, snapshot):
        # Arrange
        account_id = "12345678-1234-5678-1234-567812345680"
        user = UserFactory()
        account = AccountFactory(account_id=account_id, owner=user)

        WorkspaceFactory(account=account, is_active=True)
        WorkspaceFactory(account=account, is_active=True)
        WorkspaceFactory(account=account, is_active=False)

        storage = WorkspaceStorage()

        # Act
        result = storage.get_workspaces_by_account(
            account_id=str(account_id)
        )

        # Assert
        snapshot.assert_match(
            repr(result),
            "test_get_workspaces_by_account.txt"
        )
