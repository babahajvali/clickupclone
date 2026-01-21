import pytest

from task_management.storages.list_view_storage import ListViewStorage
from task_management.tests.factories.storage_factory import ListViewFactory, ListFactory, ViewFactory, UserFactory


class TestListViewStorage:

    @pytest.mark.django_db
    def test_apply_view_for_list_success(self, snapshot):
        # Arrange
        list_id = "12345678-1234-5678-1234-567812345678"
        view_id = "12345678-1234-5678-1234-567812345679"
        user_id = "12345678-1234-5678-1234-567812345680"
        list_obj = ListFactory(list_id=list_id)
        view = ViewFactory(view_id=view_id)
        user = UserFactory(user_id=user_id)
        storage = ListViewStorage()

        # Act
        result = storage.apply_view_for_list(list_id=str(list_id), view_id=str(view_id), user_id=str(user_id))

        # Assert
        snapshot.assert_match(repr(result), "test_apply_view_for_list_success.txt")

    @pytest.mark.django_db
    def test_remove_view_for_list_success(self, snapshot):
        # Arrange
        list_id = "12345678-1234-5678-1234-567812345678"
        view_id = "12345678-1234-5678-1234-567812345679"
        list_obj = ListFactory(list_id=list_id)
        view = ViewFactory(view_id=view_id)
        user = UserFactory()
        ListViewFactory(list=list_obj, view=view, applied_by=user, is_active=True)
        storage = ListViewStorage()

        # Act
        result = storage.remove_view_for_list(view_id=str(view_id), list_id=str(list_id))

        # Assert
        snapshot.assert_match(repr(result), "test_remove_view_for_list_success.txt")

    @pytest.mark.django_db
    def test_get_list_views_success(self, snapshot):
        # Arrange
        list_id = "12345678-1234-5678-1234-567812345678"
        list_obj = ListFactory(list_id=list_id)
        view1 = ViewFactory()
        view2 = ViewFactory()
        view3 = ViewFactory()
        user = UserFactory()
        ListViewFactory(list=list_obj, view=view1, applied_by=user, is_active=True)
        ListViewFactory(list=list_obj, view=view2, applied_by=user, is_active=True)
        ListViewFactory(list=list_obj, view=view3, applied_by=user, is_active=False)
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
        view_id = "12345678-1234-5678-1234-567812345679"
        list_obj = ListFactory(list_id=list_id)
        view = ViewFactory(view_id=view_id)
        user = UserFactory()
        ListViewFactory(list=list_obj, view=view, applied_by=user)
        storage = ListViewStorage()

        # Act
        result = storage.is_list_view_exist(list_id=str(list_id), view_id=str(view_id))

        # Assert
        snapshot.assert_match(repr(result), "test_is_list_view_exist_success.txt")

    @pytest.mark.django_db
    def test_is_list_view_exist_failure(self, snapshot):
        # Arrange
        list_id = "12345678-1234-5678-1234-567812345678"
        view_id = "12345678-1234-5678-1234-567812345679"
        storage = ListViewStorage()

        # Act
        result = storage.is_list_view_exist(list_id=str(list_id), view_id=str(view_id))

        # Assert
        snapshot.assert_match(repr(result), "test_is_list_view_exist_failure.txt")