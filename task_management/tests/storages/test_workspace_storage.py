import pytest
from factory.random import reseed_random

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
reseed_random(12345)

class TestWorkspaceStorage:

    @pytest.mark.django_db
    def test_get_workspace_success(self, snapshot):
        # Arrange
        workspace_id = "12345678-1234-5678-1234-567812345678"
        user_id = "12345678-1234-5678-1234-567812345679"
        user = UserFactory(user_id=user_id)
        account_id = "12345678-1234-5678-1234-567812345679"
        account = AccountFactory(owner=user,account_id=account_id)
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
        # snapshot.assert_match(
        #     repr(result),
        #     "test_create_workspace.txt"
        # )
        assert result.name == dto.name

    @pytest.mark.django_db
    def test_update_workspace(self, snapshot):
        # Arrange
        workspace_id = "12345678-1234-5678-1234-567812345678"
        user_id = "12345678-1234-5678-1234-567812345679"
        user = UserFactory(user_id=user_id)
        account_id = "12345678-1234-5678-1234-567812345690"
        account = AccountFactory(owner=user,account_id=account_id)
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
        user_id = "12345678-1234-5678-1234-567812345679"
        user = UserFactory(user_id=user_id)
        account_id = "12345678-1234-5678-1234-567812345690"
        account = AccountFactory(owner=user,account_id=account_id)
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
        user_id = "12345678-1234-5678-1234-567812345679"
        new_user_id = "12345678-1234-5678-1234-567812345680"
        old_owner = UserFactory(user_id=user_id)
        new_owner = UserFactory(user_id=new_user_id)
        account_id = "12345678-1234-5678-1234-567812345690"
        account = AccountFactory(owner=old_owner,account_id=account_id)

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
        user_id = "12345678-1234-5678-1234-567812345679"
        user = UserFactory(user_id=user_id)
        account = AccountFactory(account_id=account_id, owner=user)
        workspace_id1 = "12345678-1234-5678-1234-567812345679"
        workspace_id2 = "12345678-1234-5678-1234-567812345680"
        workspace_id3 = "12345678-1234-5678-1234-567812345681"

        WorkspaceFactory(workspace_id=workspace_id1,account=account, is_active=True,created_by=user)
        WorkspaceFactory(workspace_id=workspace_id2,account=account, is_active=True,created_by=user)
        WorkspaceFactory(workspace_id=workspace_id3,account=account, is_active=False,created_by=user)

        storage = WorkspaceStorage()

        # Act
        result = storage.get_active_account_workspaces(
            account_id=str(account_id)
        )

        # Assert
        snapshot.assert_match(
            repr(result),
            "test_get_workspaces_by_account.txt"
        )
