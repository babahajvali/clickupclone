import pytest
from unittest.mock import create_autospec

from task_management.exceptions.enums import Role
from task_management.interactors.dtos import (
    ListViewDTO,
    RemoveListViewDTO,
    WorkspaceMemberDTO,
)
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

        expected = ListViewDTO(
            id=1,
            list_id="d3fbf47a-7e5b-4e7f-9ca5-499d004ae545",
            view_id="baf3897a-3e70-416a-9548-5822de1b372a",
            applied_by="101fbccc-ded7-43e8-b421-eaeb534097ca",
            is_active=True,
        )
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

        expected = RemoveListViewDTO(
            id=1,
            list_id="38c1962e-9148-424f-aac1-c14f30e9c5cc",
            view_id="247a8333-f7b0-47d2-8da8-056c3d15eef7",
            removed_by="1759edc3-72ae-4244-8b01-63c1cd9d2b7d",
            is_active=False,
        )
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

        views = [
            ListViewDTO(
                id=2,
                list_id="e005b860-51ef-4922-be43-c49e149818d1",
                view_id="7d41e602-eece-428b-bf7b-118e820865d6",
                applied_by="4a84eb03-8d1f-49b7-8d2b-9deb1beb3711",
                is_active=True,
            ),
            ListViewDTO(
                id=3,
                list_id="552f233a-8c25-466a-9ff3-9849b4e1357d",
                view_id="3405095c-8a50-46c1-ac18-8efbd080e66e",
                applied_by="8c1745a7-9a6a-4f92-8ca7-4147f6be1f72",
                is_active=True,
            ),
            ListViewDTO(
                id=4,
                list_id="1775336d-71ea-4d05-89a3-e80e966e1277",
                view_id="5129fb7c-6288-41a5-8c45-782198a6416d",
                applied_by="2f120554-4a53-48cc-bdfa-bc08935ddd72",
                is_active=True,
            ),
        ]
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
