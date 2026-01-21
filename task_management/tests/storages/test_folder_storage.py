import pytest
from factory.random import reseed_random

from task_management.interactors.dtos import CreateFolderDTO, UpdateFolderDTO
from task_management.storages.folder_storage import FolderStorage
from task_management.tests.factories.storage_factory import FolderFactory, SpaceFactory, UserFactory


class TestFolderStorage:
    @pytest.fixture(autouse=True)
    def setup(self):
        """Reset faker seed before each test"""
        reseed_random(12345)
        yield

    @pytest.mark.django_db
    def test_get_folder_success(self, snapshot):
        # Arrange
        folder_id = "12345678-1234-5678-1234-567812345678"
        space_id = "12345678-1234-5678-1234-567812345679"
        user_id = "12345678-1234-5678-1234-567812345680"

        space = SpaceFactory(space_id=space_id)
        user = UserFactory(user_id=user_id)
        FolderFactory(folder_id=folder_id, space=space, created_by=user)
        storage = FolderStorage()

        # Act
        result = storage.get_folder(folder_id=str(folder_id))

        # Assert
        snapshot.assert_match(repr(result), "test_get_folder_success.txt")

    @pytest.mark.django_db
    def test_get_folder_failure(self, snapshot):
        # Arrange
        folder_id = "12345678-1234-5678-1234-567812345678"
        storage = FolderStorage()

        # Act
        result = storage.get_folder(folder_id=str(folder_id))

        # Assert
        snapshot.assert_match(repr(result), "test_get_folder_failure.txt")

    @pytest.mark.django_db
    def test_create_folder_success(self, snapshot):
        # Arrange
        space_id = "12345678-1234-5678-1234-567812345678"
        user_id = "12345678-1234-5678-1234-567812345679"
        space = SpaceFactory(space_id=space_id)
        user = UserFactory(user_id=user_id)
        create_folder_data = CreateFolderDTO(
            name="Test Folder",
            description="Test description",
            space_id=str(space_id),
            is_private=False,
            created_by=str(user_id)
        )
        storage = FolderStorage()

        # Act
        result = storage.create_folder(create_folder_data=create_folder_data)

        # Assert
        snapshot.assert_match(repr(result), "test_create_folder_success.txt")

    @pytest.mark.django_db
    def test_create_folder_with_existing_folders(self, snapshot):
        # Arrange
        space_id = "12345678-1234-5678-1234-567812345678"
        user_id = "12345678-1234-5678-1234-567812345679"
        space = SpaceFactory(space_id=space_id)
        user = UserFactory(user_id=user_id)
        FolderFactory(space=space, created_by=user, order=1)
        FolderFactory(space=space, created_by=user, order=2)
        create_folder_data = CreateFolderDTO(
            name="New Folder",
            description="New description",
            space_id=str(space_id),
            is_private=False,
            created_by=str(user_id)
        )
        storage = FolderStorage()

        # Act
        result = storage.create_folder(create_folder_data=create_folder_data)

        # Assert
        snapshot.assert_match(repr(result), "test_create_folder_with_existing_folders.txt")

    @pytest.mark.django_db
    def test_update_folder_success(self, snapshot):
        # Arrange
        folder_id = "12345678-1234-5678-1234-567812345678"
        space_id = "12345678-1234-5678-1234-567812345678"
        user_id = "12345678-1234-5678-1234-567812345679"
        space = SpaceFactory(space_id=space_id)
        user = UserFactory(user_id=user_id)
        FolderFactory(folder_id=folder_id, space=space, created_by=user, name="Old Name", description="Old description")
        update_folder_data = UpdateFolderDTO(
            folder_id=str(folder_id),
            name="New Name",
            description="New description"
        )
        storage = FolderStorage()

        # Act
        result = storage.update_folder(update_folder_data=update_folder_data)

        # Assert
        snapshot.assert_match(repr(result), "test_update_folder_success.txt")

    @pytest.mark.django_db
    def test_reorder_folder_move_down_success(self, snapshot):
        # Arrange
        folder_id = "12345678-1234-5678-1234-567812345678"
        space_id = "12345678-1234-5678-1234-567812345688"
        user_id = "12345678-1234-5678-1234-567812345679"
        space = SpaceFactory(space_id=space_id)
        user = UserFactory(user_id=user_id)
        FolderFactory(folder_id=folder_id, space=space, created_by=user, order=1)
        FolderFactory(space=space, created_by=user, order=2)
        FolderFactory(space=space, created_by=user, order=3)
        storage = FolderStorage()

        # Act
        result = storage.reorder_folder(folder_id=str(folder_id), new_order=3)

        # Assert
        snapshot.assert_match(repr(result), "test_reorder_folder_move_down_success.txt")

    @pytest.mark.django_db
    def test_reorder_folder_move_up_success(self, snapshot):
        # Arrange
        folder_id = "12345678-1234-5678-1234-567812345678"
        space_id = "12345678-1234-5678-1234-567812345688"
        user_id = "12345678-1234-5678-1234-567812345679"
        space = SpaceFactory(space_id=space_id)
        user = UserFactory(user_id=user_id)
        FolderFactory(space=space, created_by=user, order=1)
        FolderFactory(space=space, created_by=user, order=2)
        FolderFactory(folder_id=folder_id, space=space, created_by=user, order=3)
        storage = FolderStorage()

        # Act
        result = storage.reorder_folder(folder_id=str(folder_id), new_order=1)

        # Assert
        snapshot.assert_match(repr(result), "test_reorder_folder_move_up_success.txt")

    @pytest.mark.django_db
    def test_reorder_folder_same_position(self, snapshot):
        # Arrange
        folder_id = "12345678-1234-5678-1234-567812345678"
        space_id = "12345678-1234-5678-1234-567812345680"
        user_id = "12345678-1234-5678-1234-567812345679"
        space = SpaceFactory(space_id=space_id)
        user = UserFactory(user_id=user_id)
        FolderFactory(folder_id=folder_id, space=space, created_by=user, order=2)
        storage = FolderStorage()

        # Act
        result = storage.reorder_folder(folder_id=str(folder_id), new_order=2)

        # Assert
        snapshot.assert_match(repr(result), "test_reorder_folder_same_position.txt")

    @pytest.mark.django_db
    def test_remove_folder_success(self, snapshot):
        # Arrange
        folder_id = "12345678-1234-5678-1234-567812345678"
        space_id = "12345678-1234-5678-1234-567812345680"
        user_id = "12345678-1234-5678-1234-567812345679"
        space = SpaceFactory(space_id=space_id)
        user = UserFactory(user_id=user_id)
        FolderFactory(folder_id=folder_id, space=space, created_by=user, order=1, is_active=True)
        FolderFactory(space=space, created_by=user, order=2, is_active=True)
        FolderFactory(space=space, created_by=user, order=3, is_active=True)
        storage = FolderStorage()

        # Act
        result = storage.remove_folder(folder_id=str(folder_id))

        # Assert
        snapshot.assert_match(repr(result), "test_remove_folder_success.txt")

    @pytest.mark.django_db
    def test_get_space_folders_success(self, snapshot):
        # Arrange
        space_id_1 = "12345678-1234-5678-1234-567812345678"
        space_id_2 = "12345678-1234-5678-1234-567812345679"
        user_id = "12345678-1234-5678-1234-567812345680"
        space1 = SpaceFactory(space_id=space_id_1)
        space2 = SpaceFactory(space_id=space_id_2)
        user = UserFactory(user_id=user_id)
        FolderFactory(space=space1, created_by=user, is_active=True)
        FolderFactory(space=space1, created_by=user, is_active=True)
        FolderFactory(space=space2, created_by=user, is_active=True)
        FolderFactory(space=space1, created_by=user, is_active=False)
        space_ids = [str(space_id_1), str(space_id_2)]
        storage = FolderStorage()

        # Act
        result = storage.get_space_folders(space_ids=space_ids)

        # Assert
        snapshot.assert_match(repr(result), "test_get_space_folders_success.txt")

    @pytest.mark.django_db
    def test_get_space_folders_empty(self, snapshot):
        # Arrange
        space_id = "12345678-1234-5678-1234-567812345678"
        SpaceFactory(space_id=space_id)
        space_ids = [str(space_id)]
        storage = FolderStorage()

        # Act
        result = storage.get_space_folders(space_ids=space_ids)

        # Assert
        snapshot.assert_match(repr(result), "test_get_space_folders_empty.txt")

    @pytest.mark.django_db
    def test_set_folder_private_success(self, snapshot):
        # Arrange
        folder_id = "12345678-1234-5678-1234-567812345678"
        space_id = "12345678-1234-5678-1234-567812345680"
        user_id = "12345678-1234-5678-1234-567812345679"
        space = SpaceFactory(space_id=space_id)
        user = UserFactory(user_id=user_id)
        FolderFactory(folder_id=folder_id, space=space, created_by=user, is_private=False)
        storage = FolderStorage()

        # Act
        result = storage.set_folder_private(folder_id=str(folder_id))

        # Assert
        snapshot.assert_match(repr(result), "test_set_folder_private_success.txt")

    @pytest.mark.django_db
    def test_set_folder_public_success(self, snapshot):
        # Arrange
        folder_id = "12345678-1234-5678-1234-567812345678"
        space_id = "12345678-1234-5678-1234-567812345680"
        user_id = "12345678-1234-5678-1234-567812345679"
        space = SpaceFactory(space_id=space_id)
        user = UserFactory(user_id=user_id)
        FolderFactory(folder_id=folder_id, space=space, created_by=user, is_private=True)
        storage = FolderStorage()

        # Act
        result = storage.set_folder_public(folder_id=str(folder_id))

        # Assert
        snapshot.assert_match(repr(result), "test_set_folder_public_success.txt")

    @pytest.mark.django_db
    def test_get_space_folder_count_success(self, snapshot):
        # Arrange
        space_id = "12345678-1234-5678-1234-567812345680"
        user_id = "12345678-1234-5678-1234-567812345679"
        space = SpaceFactory(space_id=space_id)
        user = UserFactory(user_id=user_id)
        FolderFactory(space=space, created_by=user, is_active=True)
        FolderFactory(space=space, created_by=user, is_active=True)
        FolderFactory(space=space, created_by=user, is_active=False)
        storage = FolderStorage()

        # Act
        result = storage.get_space_folder_count(space_id=str(space_id))

        # Assert
        snapshot.assert_match(repr(result), "test_get_space_folder_count_success.txt")

    @pytest.mark.django_db
    def test_get_space_folder_count_empty(self, snapshot):
        # Arrange
        space_id = "12345678-1234-5678-1234-567812345678"
        SpaceFactory(space_id=space_id)
        storage = FolderStorage()

        # Act
        result = storage.get_space_folder_count(space_id=str(space_id))

        # Assert
        snapshot.assert_match(repr(result), "test_get_space_folder_count_empty.txt")