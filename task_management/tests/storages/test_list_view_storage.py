import pytest

from task_management.exceptions.enums import ViewType
from task_management.interactors.dtos import CreateListViewDTO
from task_management.storages.list_view_storage import ListViewStorage
from task_management.tests.factories.storage_factory import ListViewFactory, \
    ListFactory, UserFactory


class TestListViewStorage:

    @pytest.mark.django_db
    def test_apply_view_for_list_success(self, snapshot):
        # Arrange
        list_id = "12345678-1234-5678-1234-567812345678"
        user_id = "12345678-1234-5678-1234-567812345680"
        ListFactory(list_id=list_id)
        UserFactory(user_id=user_id)
        storage = ListViewStorage()

        create_dto = CreateListViewDTO(
            view_name="Table View",
            list_id=list_id,
            view_type=ViewType.TABLE,
            created_by=user_id
        )

        # Act
        result = storage.create_list_view(create_list_view_dto=create_dto)

        # Assert
        snapshot.assert_match(repr(result),
                              "test_apply_view_for_list_success.txt")

    @pytest.mark.django_db
    def test_remove_view_for_list_success(self, snapshot):
        # Arrange
        list_id = "12345678-1234-5678-1234-567812345678"
        user_id = "12345678-1234-5678-1234-567812345680"
        list_obj = ListFactory(list_id=list_id)
        user = UserFactory(user_id=user_id)
        list_view = ListViewFactory(list=list_obj,
                                    view_type=ViewType.TABLE.value,
                                    created_by=user, is_active=True)
        storage = ListViewStorage()

        # Act
        result = storage.remove_list_view(list_view_id=list_view.id)

        # Assert
        snapshot.assert_match(repr(result),
                              "test_remove_view_for_list_success.txt")

    @pytest.mark.django_db
    def test_get_list_views_success(self, snapshot):
        # Arrange
        list_id = "12345678-1234-5678-1234-567812345678"
        user_id = "12345678-1234-5678-1234-567812345680"
        list_obj = ListFactory(list_id=list_id)
        user = UserFactory(user_id=user_id)
        ListViewFactory(list=list_obj, view_type=ViewType.TABLE.value,
                        created_by=user, is_active=True)
        ListViewFactory(list=list_obj, view_type=ViewType.BOARD.value,
                        created_by=user, is_active=True)
        ListViewFactory(list=list_obj, view_type=ViewType.CALENDAR.value,
                        created_by=user, is_active=False)
        storage = ListViewStorage()

        # Act
        result = storage.get_list_views(list_id=str(list_id))

        # Assert
        snapshot.assert_match(repr(result), "test_get_list_views_success.txt")

    @pytest.mark.django_db
    def test_get_list_views_empty(self, snapshot):
        # Arrange
        list_id = "12345678-1234-5678-1234-567812345678"
        ListFactory(list_id=list_id)
        storage = ListViewStorage()

        # Act
        result = storage.get_list_views(list_id=str(list_id))

        # Assert
        snapshot.assert_match(repr(result), "test_get_list_views_empty.txt")

    @pytest.mark.django_db
    def test_is_list_view_exist_success(self, snapshot):
        # Arrange
        list_id = "12345678-1234-5678-1234-567812345678"
        list_obj = ListFactory(list_id=list_id)
        user = UserFactory()
        list_view = ListViewFactory(list=list_obj,
                                    view_type=ViewType.TABLE.value,
                                    created_by=user)
        storage = ListViewStorage()

        # Act
        result = storage.is_list_view_exist(list_view_id=list_view.id)

        # Assert
        snapshot.assert_match(repr(result),
                              "test_is_list_view_exist_success.txt")

    @pytest.mark.django_db
    def test_is_list_view_exist_failure(self, snapshot):
        # Arrange
        list_id = "12345678-1234-5678-1234-567812345678"
        view_id = "12345678-1234-5678-1234-567812345679"
        storage = ListViewStorage()

        # Act
        result = storage.is_list_view_exist(list_view_id=1)

        # Assert
        snapshot.assert_match(
            repr(result), "test_is_list_view_exist_failure.txt")
