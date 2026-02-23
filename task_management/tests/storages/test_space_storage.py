import pytest

from task_management.interactors.dtos import CreateSpaceDTO, UpdateSpaceDTO
from task_management.storages.space_storage import SpaceStorage
from task_management.tests.factories.storage_factory import SpaceFactory, \
    WorkspaceFactory, UserFactory


class TestSpaceStorage:

    @pytest.mark.django_db
    def test_get_space_success(self, snapshot):
        # Arrange
        space_id = "12345678-1234-5678-1234-567812345678"
        user_id = "12345678-1234-5678-1234-567812345679"
        workspace_id = "12345678-1234-5678-1234-567812345679"
        workspace = WorkspaceFactory(workspace_id=workspace_id)
        user = UserFactory(user_id=user_id)
        SpaceFactory(space_id=space_id, workspace=workspace, created_by=user)
        storage = SpaceStorage()

        # Act
        result = storage.get_space(space_id=str(space_id))

        # Assert
        snapshot.assert_match(repr(result), "test_get_space_success.txt")

    @pytest.mark.django_db
    def test_get_space_failure(self, snapshot):
        # Arrange
        space_id = "12345678-1234-5678-1234-567812345678"
        storage = SpaceStorage()

        # Act
        result = storage.get_space(space_id=str(space_id))

        # Assert
        snapshot.assert_match(repr(result), "test_get_space_failure.txt")

    @pytest.mark.django_db
    def test_create_space_success(self, snapshot):
        # Arrange
        workspace_id = "12345678-1234-5678-1234-567812345678"
        user_id = "12345678-1234-5678-1234-567812345679"
        workspace = WorkspaceFactory(workspace_id=workspace_id)
        user = UserFactory(user_id=user_id)
        create_space_data = CreateSpaceDTO(
            name="Test Space",
            description="Test description",
            workspace_id=str(workspace_id),
            is_private=False,
            created_by=str(user_id)
        )
        storage = SpaceStorage()

        # Act
        result = storage.create_space(space_data=create_space_data, order=1)

        # Assert
        snapshot.assert_match(repr(result), "test_create_space_success.txt")

    @pytest.mark.django_db
    def test_create_space_with_existing_spaces(self, snapshot):
        # Arrange
        workspace_id = "12345678-1234-5678-1234-567812345678"
        user_id = "12345678-1234-5678-1234-567812345679"
        workspace = WorkspaceFactory(workspace_id=workspace_id)
        user = UserFactory(user_id=user_id)
        SpaceFactory(workspace=workspace, created_by=user, order=1)
        SpaceFactory(workspace=workspace, created_by=user, order=2)
        create_space_data = CreateSpaceDTO(
            name="New Space",
            description="New description",
            workspace_id=str(workspace_id),
            is_private=False,
            created_by=str(user_id)
        )
        storage = SpaceStorage()

        # Act
        result = storage.create_space(space_data=create_space_data, order=1)

        # Assert
        snapshot.assert_match(repr(result),
                              "test_create_space_with_existing_spaces.txt")

    @pytest.mark.django_db
    def test_update_space_success(self, snapshot):
        # Arrange
        space_id = "12345678-1234-5678-1234-567812345678"
        user_id = "12345678-1234-5678-1234-567812345679"
        workspace_id = "12345678-1234-5678-1234-567812345679"
        workspace = WorkspaceFactory(workspace_id=workspace_id)
        user = UserFactory(user_id=user_id)
        SpaceFactory(space_id=space_id, workspace=workspace, created_by=user,
                     name="Old Name", description="Old description")
        space_id = str(space_id)
        name = "New Name"
        description = "New description"

        storage = SpaceStorage()

        # Act
        result = storage.update_space(
            space_id=space_id, name=name, description=description)

        # Assert
        snapshot.assert_match(repr(result), "test_update_space_success.txt")

    @pytest.mark.django_db
    def test_remove_space_success(self, snapshot):
        # Arrange
        space_id = "12345678-1234-5678-1234-567812345678"
        user_id = "12345678-1234-5678-1234-567812345679"
        workspace_id = "12345678-1234-5678-1234-567812345679"
        workspace = WorkspaceFactory(workspace_id=workspace_id)
        user = UserFactory(user_id=user_id)
        SpaceFactory(space_id=space_id, workspace=workspace, created_by=user,
                     order=1, is_deleted=False)
        SpaceFactory(workspace=workspace, created_by=user, order=2,
                     is_deleted=False)
        SpaceFactory(workspace=workspace, created_by=user, order=3,
                     is_deleted=False)
        storage = SpaceStorage()

        # Act
        result = storage.delete_space(space_id=str(space_id))

        # Assert
        snapshot.assert_match(repr(result), "test_remove_space_success.txt")

    @pytest.mark.django_db
    def test_update_space_public_success(self, snapshot):
        # Arrange
        space_id = "12345678-1234-5678-1234-567812345678"
        user_id = "12345678-1234-5678-1234-567812345679"
        workspace_id = "12345678-1234-5678-1234-567812345679"
        workspace = WorkspaceFactory(workspace_id=workspace_id)
        user = UserFactory(user_id=user_id)
        SpaceFactory(space_id=space_id, workspace=workspace, created_by=user,
                     is_private=True)
        storage = SpaceStorage()

        # Act
        result = storage.update_space_visibility(space_id=str(space_id),
                                                 visibility="PUBLIC")

        # Assert
        snapshot.assert_match(repr(result),
                              "test_set_space_public_success.txt")

    @pytest.mark.django_db
    def test_update_space_private_success(self, snapshot):
        # Arrange
        space_id = "12345678-1234-5678-1234-567812345678"
        user_id = "12345678-1234-5678-1234-567812345679"
        workspace_id = "12345678-1234-5678-1234-567812345679"
        workspace = WorkspaceFactory(workspace_id=workspace_id)
        user = UserFactory(user_id=user_id)
        SpaceFactory(space_id=space_id, workspace=workspace, created_by=user,
                     is_private=True)
        storage = SpaceStorage()

        # Act
        result = storage.update_space_visibility(space_id=str(space_id),
                                                 visibility="PRIVATE")

        # Assert
        snapshot.assert_match(repr(result),
                              "test_set_space_public_success.txt")

    @pytest.mark.django_db
    def test_get_workspace_spaces_success(self, snapshot):
        # Arrange
        space_id1 = "12345678-1234-5678-1234-567812345679"
        space_id2 = "12345678-1234-5678-1234-567812345680"
        space_id3 = "12345678-1234-5678-1234-567812345681"
        user_id = "12345678-1234-5678-1234-567812345679"
        workspace_id = "12345678-1234-5678-1234-567812345679"
        workspace = WorkspaceFactory(workspace_id=workspace_id)
        user = UserFactory(user_id=user_id)
        SpaceFactory(space_id=space_id1, workspace=workspace, created_by=user,
                     is_deleted=False)
        SpaceFactory(space_id=space_id2, workspace=workspace, created_by=user,
                     is_deleted=False)
        SpaceFactory(space_id=space_id3, workspace=workspace, created_by=user,
                     is_deleted=True)
        storage = SpaceStorage()

        # Act
        result = storage.get_workspace_spaces(
            workspace_id=str(workspace_id))

        # Assert
        snapshot.assert_match(repr(result),
                              "test_get_workspace_spaces_success.txt")

    @pytest.mark.django_db
    def test_get_workspace_spaces_empty(self, snapshot):
        # Arrange
        workspace_id = "12345678-1234-5678-1234-567812345678"
        WorkspaceFactory(workspace_id=workspace_id)
        storage = SpaceStorage()

        # Act
        result = storage.get_workspace_spaces(
            workspace_id=str(workspace_id))

        # Assert
        snapshot.assert_match(repr(result),
                              "test_get_workspace_spaces_empty.txt")

    @pytest.mark.django_db
    def test_get_workspace_spaces_count_success(self, snapshot):
        # Arrange
        user_id = "12345678-1234-5678-1234-567812345679"
        workspace_id = "12345678-1234-5678-1234-567812345679"
        workspace = WorkspaceFactory(workspace_id=workspace_id)
        user = UserFactory(user_id=user_id)
        SpaceFactory(workspace=workspace, created_by=user, is_deleted=False)
        SpaceFactory(workspace=workspace, created_by=user, is_deleted=False)
        SpaceFactory(workspace=workspace, created_by=user, is_deleted=True)
        storage = SpaceStorage()

        # Act
        result = storage.get_workspace_spaces_count(
            workspace_id=str(workspace_id))

        # Assert
        snapshot.assert_match(repr(result),
                              "test_get_workspace_spaces_count_success.txt")

    @pytest.mark.django_db
    def test_get_workspace_spaces_count_empty(self, snapshot):
        # Arrange
        workspace_id = "12345678-1234-5678-1234-567812345678"
        WorkspaceFactory(workspace_id=workspace_id)
        storage = SpaceStorage()

        # Act
        result = storage.get_workspace_spaces_count(
            workspace_id=str(workspace_id))

        # Assert
        snapshot.assert_match(repr(result),
                              "test_get_workspace_spaces_count_empty.txt")
