import pytest

from task_management.interactors.dtos import CreateListDTO, UpdateListDTO
from task_management.storages.list_storage import ListStorage
from task_management.tests.factories.storage_factory import ListFactory, \
    TemplateFactory, SpaceFactory, FolderFactory, UserFactory


class TestListStorage:

    @pytest.mark.django_db
    def test_get_template_id_by_list_id_success(self, snapshot):
        # Arrange
        list_id = "12345678-1234-5678-1234-567812345678"
        template_id = "12345678-1234-5678-1234-567812345679"
        list_obj = ListFactory(list_id=list_id)
        TemplateFactory(template_id=template_id, list=list_obj)
        storage = ListStorage()

        # Act
        result = storage.get_template_id_by_list_id(list_id=str(list_id))

        # Assert
        snapshot.assert_match(repr(result),
                              "test_get_template_id_by_list_id_success.txt")

    @pytest.mark.django_db
    def test_get_list_success(self, snapshot):
        # Arrange
        list_id = "12345678-1234-5678-1234-567812345678"
        space_id = "12345678-1234-5678-1234-567812345679"
        folder_id = "12345678-1234-5678-1234-567812345680"
        user_id = "12345678-1234-5678-1234-567812345681"
        space = SpaceFactory(space_id=space_id)
        folder = FolderFactory(folder_id=folder_id)
        user = UserFactory(user_id=user_id)
        ListFactory(list_id=list_id, space=space, folder=folder,
                    created_by=user)
        storage = ListStorage()

        # Act
        result = storage.get_list(list_id=str(list_id))

        # Assert
        snapshot.assert_match(repr(result), "test_get_list_success.txt")

    @pytest.mark.django_db
    def test_get_list_failure(self, snapshot):
        # Arrange
        list_id = "12345678-1234-5678-1234-567812345678"
        storage = ListStorage()

        # Act
        result = storage.get_list(list_id=str(list_id))

        # Assert
        snapshot.assert_match(repr(result), "test_get_list_failure.txt")

    @pytest.mark.django_db
    def test_create_list_with_folder_success(self, snapshot):
        # Arrange
        space_id = "12345678-1234-5678-1234-567812345678"
        folder_id = "12345678-1234-5678-1234-567812345679"
        user_id = "12345678-1234-5678-1234-567812345680"
        space = SpaceFactory(space_id=space_id)
        folder = FolderFactory(folder_id=folder_id, space=space)
        user = UserFactory(user_id=user_id)
        create_list_data = CreateListDTO(
            name="Test List",
            description="Test description",
            space_id=str(space_id),
            folder_id=str(folder_id),
            is_private=False,
            created_by=str(user_id)
        )
        storage = ListStorage()

        # Act
        result = storage.create_list(list_data=create_list_data)

        # Assert
        # snapshot.assert_match(repr(result), "test_create_list_with_folder_success.txt")
        assert result.name == create_list_data.name
        assert result.description == create_list_data.description

    @pytest.mark.django_db
    def test_create_list_without_folder_success(self, snapshot):
        # Arrange
        space_id = "12345678-1234-5678-1234-567812345678"
        user_id = "12345678-1234-5678-1234-567812345680"
        space = SpaceFactory(space_id=space_id)
        user = UserFactory(user_id=user_id)
        create_list_data = CreateListDTO(
            name="Test List",
            description="Test description",
            space_id=str(space_id),
            folder_id=None,
            is_private=False,
            created_by=str(user_id)
        )
        storage = ListStorage()

        # Act
        result = storage.create_list(list_data=create_list_data)

        # Assert
        # snapshot.assert_match(repr(result), "test_create_list_without_folder_success.txt")
        assert result.folder_id == create_list_data.folder_id
        assert result.name == create_list_data.name
        assert result.description == create_list_data.description

    @pytest.mark.django_db
    def test_create_list_with_existing_lists_in_folder(self, snapshot):
        # Arrange
        space_id = "12345678-1234-5678-1234-567812345678"
        folder_id = "12345678-1234-5678-1234-567812345679"
        user_id = "12345678-1234-5678-1234-567812345680"
        space = SpaceFactory(space_id=space_id)
        folder = FolderFactory(folder_id=folder_id, space=space)
        user = UserFactory(user_id=user_id)
        ListFactory(space=space, folder=folder, created_by=user, order=1)
        ListFactory(space=space, folder=folder, created_by=user, order=2)
        create_list_data = CreateListDTO(
            name="New List",
            description="New description",
            space_id=str(space_id),
            folder_id=str(folder_id),
            is_private=False,
            created_by=str(user_id)
        )
        storage = ListStorage()

        # Act
        result = storage.create_list(list_data=create_list_data)

        # Assert
        # snapshot.assert_match(repr(result), "test_create_list_with_existing_lists_in_folder.txt")
        assert result.name == create_list_data.name

    @pytest.mark.django_db
    def test_update_list_success(self, snapshot):
        # Arrange
        list_id = "12345678-1234-5678-1234-567812345678"
        space_id = "12345678-1234-5678-1234-567812345679"
        folder_id = "12345678-1234-5678-1234-567812345678"
        user_id = "12345678-1234-5678-1234-567812345681"
        space = SpaceFactory(space_id=space_id)
        user = UserFactory(user_id=user_id)
        folder = FolderFactory(folder_id=folder_id, space=space)
        ListFactory(list_id=list_id, folder=folder, space=space,
                    created_by=user, name="Old Name",
                    description="Old description")
        list_id = str(list_id)
        name = "New Name"
        description = "New description"

        storage = ListStorage()

        # Act
        result = storage.update_list(
            list_id=list_id, field_properties={"name": name,
                                                      "description": description})

        # Assert
        snapshot.assert_match(repr(result), "test_update_list_success.txt")

    @pytest.mark.django_db
    def test_get_folder_lists_success(self, snapshot):
        # Arrange
        folder_id_1 = "12345678-1234-5678-1234-567812345678"
        folder_id_2 = "12345678-1234-5678-1234-567812345679"
        space_id = "12345678-1234-5678-1234-567812345680"
        user_id = "12345678-1234-5678-1234-567812345681"
        space = SpaceFactory(space_id=space_id)
        folder1 = FolderFactory(folder_id=folder_id_1, space=space)
        folder2 = FolderFactory(folder_id=folder_id_2, space=space)
        user = UserFactory(user_id=user_id)
        ListFactory(list_id="12345678-1234-5678-1234-567812345681",
                    space=space, folder=folder1, created_by=user,
                    is_active=True)
        ListFactory(list_id="12345678-1234-5678-1234-567812345682",
                    space=space, folder=folder1, created_by=user,
                    is_active=True)
        ListFactory(list_id="12345678-1234-5678-1234-567812345683",
                    space=space, folder=folder2, created_by=user,
                    is_active=True)
        ListFactory(list_id="12345678-1234-5678-1234-567812345684",
                    space=space, folder=folder1, created_by=user,
                    is_active=False)
        folder_ids = [str(folder_id_1), str(folder_id_2)]
        storage = ListStorage()

        # Act
        result = storage.get_active_folder_lists(folder_ids=folder_ids)

        # Assert
        snapshot.assert_match(repr(result),
                              "test_get_folder_lists_success.txt")

    @pytest.mark.django_db
    def test_get_folder_lists_empty(self, snapshot):
        # Arrange
        folder_id = "12345678-1234-5678-1234-567812345678"
        space = SpaceFactory()
        FolderFactory(folder_id=folder_id, space=space)
        folder_ids = [str(folder_id)]
        storage = ListStorage()

        # Act
        result = storage.get_active_folder_lists(folder_ids=folder_ids)

        # Assert
        snapshot.assert_match(repr(result), "test_get_folder_lists_empty.txt")

    @pytest.mark.django_db
    def test_get_space_lists_success(self, snapshot):
        # Arrange
        space_id_1 = "12345678-1234-5678-1234-567812345678"
        space_id_2 = "12345678-1234-5678-1234-567812345679"
        user_id = "12345678-1234-5678-1234-567812345681"
        space1 = SpaceFactory(space_id=space_id_1)
        space2 = SpaceFactory(space_id=space_id_2)
        user = UserFactory(user_id=user_id)
        ListFactory(list_id="12345678-1234-5678-1234-567812345681",
                    space=space1, folder=None, created_by=user, is_active=True)
        ListFactory(list_id="12345678-1234-5678-1234-567812345682",
                    space=space1, folder=None, created_by=user, is_active=True)
        ListFactory(list_id="12345678-1234-5678-1234-567812345683",
                    space=space2, folder=None, created_by=user, is_active=True)
        ListFactory(list_id="12345678-1234-5678-1234-567812345684",
                    space=space1, folder=None, created_by=user,
                    is_active=False)
        space_ids = [str(space_id_1), str(space_id_2)]
        storage = ListStorage()

        # Act
        result = storage.get_active_space_lists(space_ids=space_ids)

        # Assert
        snapshot.assert_match(repr(result), "test_get_space_lists_success.txt")

    @pytest.mark.django_db
    def test_get_space_lists_empty(self, snapshot):
        # Arrange
        space_id = "12345678-1234-5678-1234-567812345678"
        SpaceFactory(space_id=space_id)
        space_ids = [str(space_id)]
        storage = ListStorage()

        # Act
        result = storage.get_active_space_lists(space_ids=space_ids)

        # Assert
        snapshot.assert_match(repr(result), "test_get_space_lists_empty.txt")

    @pytest.mark.django_db
    def test_remove_list_with_folder_success(self, snapshot):
        # Arrange
        list_id = "12345678-1234-5678-1234-567812345678"
        folder_id = "12345678-1234-5678-1234-567812345679"
        space_id = "12345678-1234-5678-1234-567812345680"
        user_id = "12345678-1234-5678-1234-567812345681"
        space = SpaceFactory(space_id=space_id)
        folder = FolderFactory(folder_id=folder_id, space=space)
        user = UserFactory(user_id=user_id)
        ListFactory(list_id=list_id, space=space, folder=folder,
                    created_by=user, order=1, is_active=True)
        ListFactory(space=space, folder=folder, created_by=user, order=2,
                    is_active=True)
        ListFactory(space=space, folder=folder, created_by=user, order=3,
                    is_active=True)
        storage = ListStorage()

        # Act
        result = storage.delete_list(list_id=str(list_id))

        # Assert
        snapshot.assert_match(repr(result),
                              "test_remove_list_with_folder_success.txt")

    @pytest.mark.django_db
    def test_remove_list_without_folder_success(self, snapshot):
        # Arrange
        list_id = "12345678-1234-5678-1234-567812345678"
        space_id = "12345678-1234-5678-1234-567812345679"
        user_id = "12345678-1234-5678-1234-567812345681"
        space = SpaceFactory(space_id=space_id)
        user = UserFactory(user_id=user_id)
        ListFactory(list_id=list_id, space=space, folder=None, created_by=user,
                    order=1, is_active=True)
        ListFactory(space=space, folder=None, created_by=user, order=2,
                    is_active=True)
        ListFactory(space=space, folder=None, created_by=user, order=3,
                    is_active=True)
        storage = ListStorage()

        # Act
        result = storage.delete_list(list_id=str(list_id))

        # Assert
        snapshot.assert_match(repr(result),
                              "test_remove_list_without_folder_success.txt")

    @pytest.mark.django_db
    def test_make_list_private_success(self, snapshot):
        # Arrange
        list_id = "12345678-1234-5678-1234-567812345678"
        folder_id = "12345678-1234-5678-1234-567812345679"
        space_id = "12345678-1234-5678-1234-567812345679"
        user_id = "12345678-1234-5678-1234-567812345681"
        space = SpaceFactory(space_id=space_id)
        folder = FolderFactory(folder_id=folder_id, space=space)
        user = UserFactory(user_id=user_id)
        ListFactory(list_id=list_id, space=space, created_by=user,
                    is_private=False, folder=folder)
        storage = ListStorage()

        # Act
        result = storage.make_list_private(list_id=str(list_id))

        # Assert
        snapshot.assert_match(repr(result),
                              "test_make_list_private_success.txt")

    @pytest.mark.django_db
    def test_make_list_public_success(self, snapshot):
        # Arrange
        list_id = "12345678-1234-5678-1234-567812345678"
        folder_id = "12345678-1234-5678-1234-567812345679"
        space_id = "12345678-1234-5678-1234-567812345679"
        user_id = "12345678-1234-5678-1234-567812345681"
        space = SpaceFactory(space_id=space_id)
        folder = FolderFactory(folder_id=folder_id, space=space)
        user = UserFactory(user_id=user_id)
        ListFactory(list_id=list_id, space=space, created_by=user,
                    is_private=True, folder=folder)
        storage = ListStorage()

        # Act
        result = storage.make_list_public(list_id=str(list_id))

        # Assert
        snapshot.assert_match(repr(result),
                              "test_make_list_public_success.txt")

    @pytest.mark.django_db
    def test_reorder_list_in_folder_move_down_success(self, snapshot):
        # Arrange
        list_id = "12345678-1234-5678-1234-567812345678"
        folder_id = "12345678-1234-5678-1234-567812345679"
        space_id = "12345678-1234-5678-1234-567812345679"
        user_id = "12345678-1234-5678-1234-567812345681"
        space = SpaceFactory(space_id=space_id)
        user = UserFactory(user_id=user_id)
        folder = FolderFactory(folder_id=folder_id, space=space)
        ListFactory(list_id=list_id, space=space, folder=folder,
                    created_by=user, order=1)
        ListFactory(space=space, folder=folder, created_by=user, order=2)
        ListFactory(space=space, folder=folder, created_by=user, order=3)
        storage = ListStorage()

        # Act
        result = storage.reorder_list_in_folder(folder_id=str(folder_id),
                                                list_id=str(list_id), order=3)

        # Assert
        snapshot.assert_match(repr(result),
                              "test_reorder_list_in_folder_move_down_success.txt")

    @pytest.mark.django_db
    def test_reorder_list_in_folder_move_up_success(self, snapshot):
        # Arrange
        list_id = "12345678-1234-5678-1234-567812345678"
        folder_id = "12345678-1234-5678-1234-567812345679"
        space_id = "12345678-1234-5678-1234-567812345679"
        user_id = "12345678-1234-5678-1234-567812345681"
        space = SpaceFactory(space_id=space_id)
        user = UserFactory(user_id=user_id)
        folder = FolderFactory(folder_id=folder_id, space=space)
        ListFactory(space=space, folder=folder, created_by=user, order=1)
        ListFactory(space=space, folder=folder, created_by=user, order=2)
        ListFactory(list_id=list_id, space=space, folder=folder,
                    created_by=user, order=3)
        storage = ListStorage()

        # Act
        result = storage.reorder_list_in_folder(folder_id=str(folder_id),
                                                list_id=str(list_id), order=1)

        # Assert
        snapshot.assert_match(repr(result),
                              "test_reorder_list_in_folder_move_up_success.txt")

    @pytest.mark.django_db
    def test_reorder_list_in_folder_same_position(self, snapshot):
        # Arrange
        list_id = "12345678-1234-5678-1234-567812345678"
        folder_id = "12345678-1234-5678-1234-567812345679"
        space_id = "12345678-1234-5678-1234-567812345679"
        user_id = "12345678-1234-5678-1234-567812345681"
        space = SpaceFactory(space_id=space_id)
        user = UserFactory(user_id=user_id)
        folder = FolderFactory(folder_id=folder_id, space=space)
        ListFactory(list_id=list_id, space=space, folder=folder,
                    created_by=user, order=2)
        storage = ListStorage()

        # Act
        result = storage.reorder_list_in_folder(folder_id=str(folder_id),
                                                list_id=str(list_id), order=2)

        # Assert
        snapshot.assert_match(repr(result),
                              "test_reorder_list_in_folder_same_position.txt")

    @pytest.mark.django_db
    def test_reorder_list_in_space_move_down_success(self, snapshot):
        # Arrange
        list_id = "12345678-1234-5678-1234-567812345678"
        space_id = "12345678-1234-5678-1234-567812345679"
        user_id = "12345678-1234-5678-1234-567812345681"
        space = SpaceFactory(space_id=space_id)
        user = UserFactory(user_id=user_id)
        ListFactory(list_id=list_id, space=space, folder=None, created_by=user,
                    order=1)
        ListFactory(space=space, folder=None, created_by=user, order=2)
        ListFactory(space=space, folder=None, created_by=user, order=3)
        storage = ListStorage()

        # Act
        result = storage.reorder_list_in_space(space_id=str(space_id),
                                               list_id=str(list_id), order=3)

        # Assert
        snapshot.assert_match(repr(result),
                              "test_reorder_list_in_space_move_down_success.txt")

    @pytest.mark.django_db
    def test_reorder_list_in_space_move_up_success(self, snapshot):
        # Arrange
        list_id = "12345678-1234-5678-1234-567812345678"
        space_id = "12345678-1234-5678-1234-567812345679"
        user_id = "12345678-1234-5678-1234-567812345681"
        space = SpaceFactory(space_id=space_id)
        user = UserFactory(user_id=user_id)
        ListFactory(space=space, folder=None, created_by=user, order=1)
        ListFactory(space=space, folder=None, created_by=user, order=2)
        ListFactory(list_id=list_id, space=space, folder=None, created_by=user,
                    order=3)
        storage = ListStorage()

        # Act
        result = storage.reorder_list_in_space(space_id=str(space_id),
                                               list_id=str(list_id), order=1)

        # Assert
        snapshot.assert_match(repr(result),
                              "test_reorder_list_in_space_move_up_success.txt")

    @pytest.mark.django_db
    def test_reorder_list_in_space_same_position(self, snapshot):
        # Arrange
        list_id = "12345678-1234-5678-1234-567812345678"
        space_id = "12345678-1234-5678-1234-567812345679"
        user_id = "12345678-1234-5678-1234-567812345681"
        space = SpaceFactory(space_id=space_id)
        user = UserFactory(user_id=user_id)
        ListFactory(list_id=list_id, space=space, folder=None, created_by=user,
                    order=2)
        storage = ListStorage()

        # Act
        result = storage.reorder_list_in_space(space_id=str(space_id),
                                               list_id=str(list_id), order=2)

        # Assert
        snapshot.assert_match(repr(result),
                              "test_reorder_list_in_space_same_position.txt")

    @pytest.mark.django_db
    def test_get_folder_lists_count_success(self, snapshot):
        # Arrange
        folder_id = "12345678-1234-5678-1234-567812345678"
        space_id = "12345678-1234-5678-1234-567812345679"
        user_id = "12345678-1234-5678-1234-567812345681"
        space = SpaceFactory(space_id=space_id)
        user = UserFactory(user_id=user_id)
        folder = FolderFactory(folder_id=folder_id, space=space)
        ListFactory(space=space, folder=folder, created_by=user,
                    is_active=True)
        ListFactory(space=space, folder=folder, created_by=user,
                    is_active=True)
        ListFactory(space=space, folder=folder, created_by=user,
                    is_active=False)
        storage = ListStorage()

        # Act
        result = storage.get_folder_lists_count(folder_id=str(folder_id))

        # Assert
        snapshot.assert_match(repr(result),
                              "test_get_folder_lists_count_success.txt")

    @pytest.mark.django_db
    def test_get_folder_lists_count_empty(self, snapshot):
        # Arrange
        folder_id = "12345678-1234-5678-1234-567812345678"
        space_id = "12345678-1234-5678-1234-567812345679"
        space = SpaceFactory(space_id=space_id)
        FolderFactory(folder_id=folder_id, space=space)
        storage = ListStorage()

        # Act
        result = storage.get_folder_lists_count(folder_id=str(folder_id))

        # Assert
        snapshot.assert_match(repr(result),
                              "test_get_folder_lists_count_empty.txt")

    @pytest.mark.django_db
    def test_get_space_lists_count_success(self, snapshot):
        # Arrange
        space_id = "12345678-1234-5678-1234-567812345678"
        user_id = "12345678-1234-5678-1234-567812345679"
        space = SpaceFactory(space_id=space_id)
        user = UserFactory(user_id=user_id)
        ListFactory(space=space, folder=None, created_by=user, is_active=True)
        ListFactory(space=space, folder=None, created_by=user, is_active=True)
        ListFactory(space=space, folder=None, created_by=user, is_active=False)
        storage = ListStorage()

        # Act
        result = storage.get_space_lists_count(space_id=str(space_id))

        # Assert
        snapshot.assert_match(repr(result),
                              "test_get_space_lists_count_success.txt")

    @pytest.mark.django_db
    def test_get_space_lists_count_empty(self, snapshot):
        # Arrange
        space_id = "12345678-1234-5678-1234-567812345678"
        SpaceFactory(space_id=space_id)
        storage = ListStorage()

        # Act
        result = storage.get_space_lists_count(space_id=str(space_id))

        # Assert
        snapshot.assert_match(repr(result),
                              "test_get_space_lists_count_empty.txt")
