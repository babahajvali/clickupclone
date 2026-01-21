import pytest

from task_management.exceptions.enums import Role
from task_management.interactors.dtos import AddMemberToWorkspaceDTO
from task_management.storages.workspace_member import WorkspaceMemberStorage
from task_management.tests.factories.storage_factory import WorkspaceMemberFactory, WorkspaceFactory, UserFactory


class TestWorkspaceMemberStorage:

    @pytest.mark.django_db
    def test_add_member_to_workspace_success(self, snapshot):
        # Arrange
        workspace_id = "12345678-1234-5678-1234-567812345678"
        user_id = "12345678-1234-5678-1234-567812345679"
        added_by_id = "12345678-1234-5678-1234-567812345680"
        workspace = WorkspaceFactory(workspace_id=workspace_id)
        user = UserFactory(user_id=user_id)
        added_by = UserFactory(user_id=added_by_id)
        workspace_member_data = AddMemberToWorkspaceDTO(
            workspace_id=str(workspace_id),
            user_id=str(user_id),
            added_by=str(added_by_id),
            role=Role.MEMBER
        )
        storage = WorkspaceMemberStorage()

        # Act
        result = storage.add_member_to_workspace(workspace_member_data=workspace_member_data)

        # Assert
        snapshot.assert_match(repr(result), "test_add_member_to_workspace_success.txt")

    @pytest.mark.django_db
    def test_get_workspace_member_success(self, snapshot):
        # Arrange
        workspace_id = "12345678-1234-5678-1234-567812345678"
        user_id = "12345678-1234-5678-1234-567812345679"
        workspace = WorkspaceFactory(workspace_id=workspace_id)
        user = UserFactory(user_id=user_id)
        added_by = UserFactory()
        WorkspaceMemberFactory(workspace=workspace, user=user, added_by=added_by)
        storage = WorkspaceMemberStorage()

        # Act
        result = storage.get_workspace_member(workspace_id=str(workspace_id), user_id=str(user_id))

        # Assert
        snapshot.assert_match(repr(result), "test_get_workspace_member_success.txt")

    @pytest.mark.django_db
    def test_get_workspace_member_failure(self, snapshot):
        # Arrange
        workspace_id = "12345678-1234-5678-1234-567812345678"
        user_id = "12345678-1234-5678-1234-567812345679"
        storage = WorkspaceMemberStorage()

        # Act
        result = storage.get_workspace_member(workspace_id=str(workspace_id), user_id=str(user_id))

        # Assert
        snapshot.assert_match(repr(result), "test_get_workspace_member_failure.txt")

    @pytest.mark.django_db
    def test_get_workspace_member_by_id_success(self, snapshot):
        # Arrange
        workspace = WorkspaceFactory()
        user = UserFactory()
        added_by = UserFactory()
        workspace_member = WorkspaceMemberFactory(workspace=workspace, user=user, added_by=added_by)
        storage = WorkspaceMemberStorage()

        # Act
        result = storage.get_workspace_member_by_id(workspace_member_id=workspace_member.pk)

        # Assert
        snapshot.assert_match(repr(result), "test_get_workspace_member_by_id_success.txt")

    @pytest.mark.django_db
    def test_remove_member_from_workspace_success(self, snapshot):
        # Arrange
        workspace = WorkspaceFactory()
        user = UserFactory()
        added_by = UserFactory()
        workspace_member = WorkspaceMemberFactory(workspace=workspace, user=user, added_by=added_by, is_active=True)
        storage = WorkspaceMemberStorage()

        # Act
        result = storage.remove_member_from_workspace(workspace_member_id=workspace_member.pk)

        # Assert
        snapshot.assert_match(repr(result), "test_remove_member_from_workspace_success.txt")

    @pytest.mark.django_db
    def test_update_the_member_role_success(self, snapshot):
        # Arrange
        workspace_id = "12345678-1234-5678-1234-567812345678"
        user_id = "12345678-1234-5678-1234-567812345679"
        workspace = WorkspaceFactory(workspace_id=workspace_id)
        user = UserFactory(user_id=user_id)
        added_by = UserFactory()
        WorkspaceMemberFactory(workspace=workspace, user=user, added_by=added_by, role="member")
        storage = WorkspaceMemberStorage()

        # Act
        result = storage.update_the_member_role(workspace_id=str(workspace_id), user_id=str(user_id), role="admin")

        # Assert
        snapshot.assert_match(repr(result), "test_update_the_member_role_success.txt")

    @pytest.mark.django_db
    def test_get_workspace_members_success(self, snapshot):
        # Arrange
        workspace_id = "12345678-1234-5678-1234-567812345678"
        workspace = WorkspaceFactory(workspace_id=workspace_id)
        user1 = UserFactory()
        user2 = UserFactory()
        added_by = UserFactory()
        WorkspaceMemberFactory(workspace=workspace, user=user1, added_by=added_by, is_active=True)
        WorkspaceMemberFactory(workspace=workspace, user=user2, added_by=added_by, is_active=True)
        WorkspaceMemberFactory(workspace=workspace, user=user1, added_by=added_by, is_active=False)
        storage = WorkspaceMemberStorage()

        # Act
        result = storage.get_workspace_members(workspace_id=str(workspace_id))

        # Assert
        snapshot.assert_match(repr(result), "test_get_workspace_members_success.txt")

    @pytest.mark.django_db
    def test_get_workspace_members_empty(self, snapshot):
        # Arrange
        workspace_id = "12345678-1234-5678-1234-567812345678"
        WorkspaceFactory(workspace_id=workspace_id)
        storage = WorkspaceMemberStorage()

        # Act
        result = storage.get_workspace_members(workspace_id=str(workspace_id))

        # Assert
        snapshot.assert_match(repr(result), "test_get_workspace_members_empty.txt")