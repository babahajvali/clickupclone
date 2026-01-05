import pytest
from unittest.mock import create_autospec

from task_management.exceptions.enums import PermissionsEnum
from task_management.interactors.dtos import UserListPermissionDTO
from task_management.interactors.view_interactors.list_view_interactors import (
    ListViewInteractor
)
from task_management.interactors.storage_interface.list_views_storage_interface import (
    ListViewsStorageInterface
)
from task_management.interactors.storage_interface.list_storage_interface import (
    ListStorageInterface
)
from task_management.interactors.storage_interface.view_storage_interface import (
    ViewStorageInterface
)
from task_management.interactors.storage_interface.list_permission_storage_interface import (
    ListPermissionStorageInterface
)
from task_management.exceptions.custom_exceptions import (
    NotAccessToModificationException,
    ViewNotFoundException,
    ListNotFoundException,
    InactiveListFoundException
)
from task_management.tests.factories.interactor_factory import (
    ListViewDTOFactory,
    RemoveListViewDTOFactory
)

def make_permission(permission_type: PermissionsEnum):
    return UserListPermissionDTO(
        id=1,
        list_id="list_id",
        permission_type=permission_type,
        user_id="user_id",
        is_active=True,
        added_by="admin"
    )


class TestListViewInteractor:

    def setup_method(self):
        self.list_view_storage = create_autospec(ListViewsStorageInterface)
        self.list_storage = create_autospec(ListStorageInterface)
        self.view_storage = create_autospec(ViewStorageInterface)
        self.permission_storage = create_autospec(ListPermissionStorageInterface)

        self.interactor = ListViewInteractor(
            list_view_storage=self.list_view_storage,
            list_storage=self.list_storage,
            view_storage=self.view_storage,
            permission_storage=self.permission_storage
        )

    def test_apply_view_for_list_success(self, snapshot):
        self.permission_storage.get_user_permission_for_list.return_value = (
            make_permission(PermissionsEnum.FULL_EDIT)
        )

        self.view_storage.get_view.return_value = type(
            "View", (), {"id": "view_id"}
        )()

        self.list_storage.get_list.return_value = type(
            "List", (), {"is_active": True}
        )()

        expected = ListViewDTOFactory()
        self.list_view_storage.apply_view_for_list.return_value = expected

        result = self.interactor.apply_view_for_list(
            "view_id", "list_id", "user_id"
        )

        snapshot.assert_match(repr(result), "apply_view_success.txt")

    def test_apply_view_without_permission_raises_exception(self, snapshot):
        self.permission_storage.get_user_permission_for_list.return_value = (
            make_permission(PermissionsEnum.VIEW)
        )

        with pytest.raises(NotAccessToModificationException) as exc:
            self.interactor.apply_view_for_list(
                "view_id", "list_id", "user_id"
            )

        snapshot.assert_match(repr(exc.value), "apply_permission_denied.txt")

    def test_apply_view_for_nonexistent_view_raises_exception(self, snapshot):
        self.permission_storage.get_user_permission_for_list.return_value = (
            make_permission(PermissionsEnum.FULL_EDIT)
        )

        self.view_storage.get_view.return_value = None

        with pytest.raises(ViewNotFoundException) as exc:
            self.interactor.apply_view_for_list(
                "view_id", "list_id", "user_id"
            )

        snapshot.assert_match(repr(exc.value), "apply_view_not_found.txt")

    def test_apply_view_for_nonexistent_list_raises_exception(self, snapshot):
        self.permission_storage.get_user_permission_for_list.return_value = (
            make_permission(PermissionsEnum.FULL_EDIT)
        )

        self.view_storage.get_view.return_value = type(
            "View", (), {"id": "view_id"}
        )()

        self.list_storage.get_list.return_value = None

        with pytest.raises(ListNotFoundException) as exc:
            self.interactor.apply_view_for_list(
                "view_id", "list_id", "user_id"
            )

        snapshot.assert_match(repr(exc.value), "apply_list_not_found.txt")

    def test_apply_view_for_inactive_list_raises_exception(self, snapshot):
        self.permission_storage.get_user_permission_for_list.return_value = (
            make_permission(PermissionsEnum.FULL_EDIT)
        )

        self.view_storage.get_view.return_value = type(
            "View", (), {"id": "view_id"}
        )()

        self.list_storage.get_list.return_value = type(
            "List", (), {"is_active": False}
        )()

        with pytest.raises(InactiveListFoundException) as exc:
            self.interactor.apply_view_for_list(
                "view_id", "list_id", "user_id"
            )

        snapshot.assert_match(repr(exc.value), "apply_list_inactive.txt")


    def test_remove_view_for_list_success(self, snapshot):
        self.permission_storage.get_user_permission_for_list.return_value = (
            make_permission(PermissionsEnum.FULL_EDIT)
        )

        self.view_storage.get_view.return_value = type(
            "View", (), {"id": "view_id"}
        )()

        self.list_storage.get_list.return_value = type(
            "List", (), {"is_active": True}
        )()

        expected = RemoveListViewDTOFactory()
        self.list_view_storage.remove_view_for_list.return_value = expected

        result = self.interactor.remove_view_for_list(
            "view_id", "list_id", "user_id"
        )

        snapshot.assert_match(repr(result), "remove_view_success.txt")

    def test_remove_view_without_permission_raises_exception(self, snapshot):
        self.permission_storage.get_user_permission_for_list.return_value = (
            make_permission(PermissionsEnum.VIEW)
        )

        with pytest.raises(NotAccessToModificationException) as exc:
            self.interactor.remove_view_for_list(
                "view_id", "list_id", "user_id"
            )

        snapshot.assert_match(repr(exc.value), "remove_permission_denied.txt")


    def test_get_list_views_success(self, snapshot):
        self.list_storage.get_list.return_value = type(
            "List", (), {"is_active": True}
        )()

        views = [ListViewDTOFactory() for _ in range(3)]
        self.list_view_storage.get_list_views.return_value = views

        result = self.interactor.get_list_views("list_id")

        snapshot.assert_match(repr(result), "get_list_views_success.txt")

    def test_get_views_for_inactive_list_raises_exception(self, snapshot):
        self.list_storage.get_list.return_value = type(
            "List", (), {"is_active": False}
        )()

        with pytest.raises(InactiveListFoundException) as exc:
            self.interactor.get_list_views("list_id")

        snapshot.assert_match(repr(exc.value), "get_list_inactive.txt")

    def test_get_views_for_nonexistent_list_raises_exception(self, snapshot):
        self.list_storage.get_list.return_value = None

        with pytest.raises(ListNotFoundException) as exc:
            self.interactor.get_list_views("list_id")

        snapshot.assert_match(repr(exc.value), "get_list_not_found.txt")
