import pytest

from task_management.interactors.dtos import CreateSpaceDTO
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
        SpaceFactory(
            space_id=space_id,
            workspace=workspace,
            created_by=user,
            name="Test Space",
            description="Test Description",
            order=1,
        )
        storage = SpaceStorage()

        # Act
        result = storage.get_space(space_id=str(space_id))

        # Assert
        assert result.space_id == space_id
        assert result.workspace_id == workspace_id
        assert result.created_by == user_id
        assert result.name == "Test Space"
        assert result.description == "Test Description"
        assert result.order == 1

    @pytest.mark.django_db
    def test_get_space_failure(self, snapshot):
        # Arrange
        space_id = "12345678-1234-5678-1234-567812345678"
        storage = SpaceStorage()

        # Act
        with pytest.raises(AttributeError) as exc:
            storage.get_space(space_id=str(space_id))

        # Assert
        snapshot.assert_match(repr(exc.value), "test_get_space_failure.txt")

    @pytest.mark.django_db
    def test_create_space_success(self, snapshot):
        # Arrange
        workspace_id = "12345678-1234-5678-1234-567812345678"
        user_id = "12345678-1234-5678-1234-567812345679"
        WorkspaceFactory(workspace_id=workspace_id)
        UserFactory(user_id=user_id)
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
        snapshot.assert_match(
            repr(
                {
                    "name": result.name,
                    "description": result.description,
                    "workspace_id": str(result.workspace_id),
                    "order": result.order,
                    "is_deleted": result.is_deleted,
                    "created_by": str(result.created_by),
                    "is_private": result.is_private,
                }
            ),
            "test_create_space_success.txt",
        )

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
        snapshot.assert_match(
            repr(
                {
                    "name": result.name,
                    "description": result.description,
                    "workspace_id": str(result.workspace_id),
                    "order": result.order,
                    "is_deleted": result.is_deleted,
                    "created_by": str(result.created_by),
                    "is_private": result.is_private,
                }
            ),
            "test_create_space_with_existing_spaces.txt",
        )

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
        assert result.space_id == space_id
        assert result.name == name
        assert result.description == description

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
        assert result.space_id == space_id
        assert result.is_deleted is True
        assert result.order == 1

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
        assert result.space_id == space_id
        assert result.is_private is False

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
        assert result.space_id == space_id
        assert result.is_private is True

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
        assert len(result) == 2
        result_space_ids = {space.space_id for space in result}
        assert result_space_ids == {space_id1, space_id2}

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
