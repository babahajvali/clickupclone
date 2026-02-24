import pytest
from unittest.mock import create_autospec

from task_management.exceptions.enums import Role
from task_management.interactors.dtos import WorkspaceMemberDTO
from task_management.interactors.storage_interfaces import \
    WorkspaceStorageInterface
from task_management.interactors.views.list_view_interactor import (
    ListViewInteractor
)
from task_management.interactors.storage_interfaces.list_storage_interface import (
    ListStorageInterface
)
from task_management.interactors.storage_interfaces.view_storage_interface import (
    ViewStorageInterface
)
from task_management.exceptions.custom_exceptions import (
    ModificationNotAllowed,
    ViewNotFound,
    ListNotFound,
    DeletedListFound
)
from task_management.tests.factories.interactor_factory import (
    ListViewDTOFactory,
    RemoveListViewDTOFactory
)


def make_permission(role: Role):
    return WorkspaceMemberDTO(
        id=1,
        workspace_id="workspace_id",
        role=role,
        user_id="user_id",
        is_active=True,
        added_by="admin"
    )


class TestListViewInteractor:

    def setup_method(self):
        self.list_storage = create_autospec(ListStorageInterface)
        self.view_storage = create_autospec(ViewStorageInterface)
        self.workspace_storage = create_autospec(WorkspaceStorageInterface)

        self.interactor = ListViewInteractor(
            list_storage=self.list_storage,
            view_storage=self.view_storage,
            workspace_storage=self.workspace_storage
        )

    def test_apply_view_for_list_success(self, snapshot):
        self.workspace_storage.get_workspace_member.return_value = (
            make_permission(Role.ADMIN)
        )

        self.view_storage.get_list_view.return_value = None
        self.view_storage.get_view.return_value = type(
            "View", (), {"id": "view_id"}
        )()

        self.list_storage.get_list.return_value = type(
            "List", (), {"is_deleted": False}
        )()

        expected = ListViewDTOFactory()
        self.view_storage.apply_view_for_list.return_value = expected

        result = self.interactor.apply_view_for_list(
            "view_id", "list_id", "user_id"
        )

        snapshot.assert_match(repr(result), "apply_view_success.txt")

    def test_apply_view_without_permission_raises_exception(self, snapshot):
        self.view_storage.get_list_view.return_value = None
        self.view_storage.get_view.return_value = type(
            "View", (), {"id": "view_id"}
        )()

        self.list_storage.get_list.return_value = type(
            "List", (), {"is_deleted": False}
        )()
        self.workspace_storage.get_workspace_member.return_value = (
            make_permission(Role.GUEST)
        )

        with pytest.raises(ModificationNotAllowed) as exc:
            self.interactor.apply_view_for_list(
                "view_id", "list_id", "user_id"
            )

        snapshot.assert_match(repr(exc.value), "apply_permission_denied.txt")

    def test_apply_view_for_nonexistent_view_raises_exception(self, snapshot):

        self.view_storage.get_list_view.return_value = None
        self.workspace_storage.get_workspace_member.return_value = (
            make_permission(Role.ADMIN)
        )
        self.list_storage.get_list.return_value = type(
            "List", (), {"is_deleted": False}
        )()

        self.view_storage.check_view_exists.return_value = False

        with pytest.raises(ViewNotFound) as exc:
            self.interactor.apply_view_for_list(
                "view_id", "list_id", "user_id"
            )

        snapshot.assert_match(repr(exc.value), "apply_view_not_found.txt")

    def test_apply_view_for_nonexistent_list_raises_exception(self, snapshot):
        self.view_storage.get_list_view.return_value = None
        self.workspace_storage.get_workspace_member.return_value = (
            make_permission(Role.ADMIN)
        )

        self.view_storage.get_view.return_value = type(
            "View", (), {"id": "view_id"}
        )()

        self.list_storage.get_list.return_value = None

        with pytest.raises(ListNotFound) as exc:
            self.interactor.apply_view_for_list(
                "view_id", "list_id", "user_id"
            )

        snapshot.assert_match(repr(exc.value), "apply_list_not_found.txt")

    def test_apply_view_for_inactive_list_raises_exception(self, snapshot):
        self.view_storage.get_list_view.return_value = None
        self.workspace_storage.get_workspace_member.return_value = (
            make_permission(Role.ADMIN)
        )

        self.view_storage.get_view.return_value = type(
            "View", (), {"id": "view_id"}
        )()

        self.list_storage.get_list.return_value = type(
            "List", (), {"is_deleted": True}
        )()

        with pytest.raises(DeletedListFound) as exc:
            self.interactor.apply_view_for_list(
                "view_id", "list_id", "user_id"
            )

        snapshot.assert_match(repr(exc.value), "apply_list_inactive.txt")

    def test_remove_view_for_list_success(self, snapshot):
        self.workspace_storage.get_workspace_member.return_value = (
            make_permission(Role.ADMIN)
        )

        self.view_storage.get_view.return_value = type(
            "View", (), {"id": "view_id"}
        )()

        self.list_storage.get_list.return_value = type(
            "List", (), {"is_deleted": False}
        )()

        expected = RemoveListViewDTOFactory()
        self.view_storage.remove_list_view.return_value = expected

        result = self.interactor.remove_view_for_list(
            "view_id", "list_id", "user_id"
        )

        snapshot.assert_match(repr(result), "remove_view_success.txt")

    def test_remove_view_without_permission_raises_exception(self, snapshot):
        self.view_storage.is_list_view_exist.return_value = True
        self.workspace_storage.get_workspace_member.return_value = (
            make_permission(Role.GUEST)
        )


        with pytest.raises(ModificationNotAllowed) as exc:
            self.interactor.remove_view_for_list(
                "view_id", "list_id", "user_id"
            )

        snapshot.assert_match(repr(exc.value), "remove_permission_denied.txt")

    def test_get_list_views_success(self, snapshot):
        self.list_storage.get_list.return_value = type(
            "List", (), {"is_deleted": False}
        )()

        views = [ListViewDTOFactory() for _ in range(3)]
        self.view_storage.get_list_views.return_value = views

        result = self.interactor.get_list_views("list_id")

        snapshot.assert_match(repr(result), "get_list_views_success.txt")

    def test_get_views_for_inactive_list_raises_exception(self, snapshot):
        self.list_storage.get_list.return_value = type(
            "List", (), {"is_deleted": True}
        )()

        with pytest.raises(DeletedListFound) as exc:
            self.interactor.get_list_views("list_id")

        snapshot.assert_match(repr(exc.value), "get_list_inactive.txt")

    def test_get_views_for_nonexistent_list_raises_exception(self, snapshot):
        self.list_storage.get_list.return_value = None

        with pytest.raises(ListNotFound) as exc:
            self.interactor.get_list_views("list_id")

        snapshot.assert_match(repr(exc.value), "get_list_not_found.txt")
