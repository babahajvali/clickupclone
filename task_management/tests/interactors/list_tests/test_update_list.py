import pytest
from unittest.mock import create_autospec

from task_management.exceptions.enums import Role
from task_management.interactors.dtos import WorkspaceMemberDTO
from task_management.interactors.list.list_interactor import \
    ListInteractor
from task_management.exceptions.custom_exceptions import (
    ListNotFound, InactiveList, SpaceNotFound,
    ModificationNotAllowed,
)
from task_management.interactors.storage_interfaces import \
    ListStorageInterface, FolderStorageInterface, SpaceStorageInterface, \
    WorkspaceStorageInterface
from task_management.tests.factories.interactor_factory import \
    UpdateListDTOFactory


def make_permission(role: Role):
    return WorkspaceMemberDTO(
        id=1,
        workspace_id="workspace_id1",
        role=role,
        user_id="user_id",
        is_active=True,
        added_by="admin"
    )


class TestUpdateList:

    def setup_method(self):
        self.list_storage = create_autospec(ListStorageInterface)
        self.folder_storage = create_autospec(FolderStorageInterface)
        self.space_storage = create_autospec(SpaceStorageInterface)
        self.workspace_storage = create_autospec(WorkspaceStorageInterface)

        self.interactor = ListInteractor(
            list_storage=self.list_storage,
            folder_storage=self.folder_storage,
            space_storage=self.space_storage,
            workspace_storage=self.workspace_storage
        )

    def test_update_list_success(self, snapshot):
        dto = UpdateListDTOFactory()

        self.interactor.list_storage.get_list.return_value = type("List", (), {
            "is_active": True,
            "folder_id": None,
            "space_id": "space_1", }, )()
        self.workspace_member_storage.get_workspace_member.return_value = (
            make_permission(Role.MEMBER)
        )

        self.interactor.space_storage.get_space.return_value = type("Space",
                                                                    (), {
                                                                        "is_active": True, }, )()
        self.interactor.list_storage.get_folder_lists_count.return_value = 100
        self.interactor.list_storage.update_list.return_value = "UPDATED_LIST_DTO"

        result = self.interactor.update_list(dto, user_id="user_id1")

        snapshot.assert_match(
            repr(result),
            "update_list_success.json"
        )

    def test_list_not_found(self, snapshot):
        dto = UpdateListDTOFactory()
        self.interactor.list_storage.get_list.return_value = None

        with pytest.raises(ListNotFound) as exc:
            self.interactor.update_list(dto, user_id="user_id")

        snapshot.assert_match(repr(exc.value), "list_not_found.txt")

    def test_list_inactive(self, snapshot):
        dto = UpdateListDTOFactory()
        self.interactor.list_storage.get_list.return_value = type(
            "List", (), {"is_active": False}
        )()

        with pytest.raises(InactiveList) as exc:
            self.interactor.update_list(dto, user_id="user_id")

        snapshot.assert_match(repr(exc.value), "list_inactive.txt")

    def test_permission_denied(self, snapshot):
        dto = UpdateListDTOFactory()
        folder_id = 'folder_id1'
        self.interactor.list_storage.get_list.return_value = type(
            "List", (), {"is_active": True,"folder_id":folder_id,"space_id": "space_1", },
        )()
        self.workspace_member_storage.get_workspace_member.return_value = (
            make_permission(Role.GUEST)
        )

        with pytest.raises(ModificationNotAllowed) as exc:
            self.interactor.update_list(dto, user_id="user_id")

        snapshot.assert_match(repr(exc.value), "permission_denied.txt")

    def test_space_not_found(self, snapshot):
        dto = UpdateListDTOFactory()
        self.interactor.list_storage.get_list.return_value = type("List", (), {
            "is_active": True,
            "folder_id": None,
            "space_id": "space_1", }, )()

        self.workspace_member_storage.get_workspace_member.return_value = (
            make_permission(Role.MEMBER)
        )
        self.interactor.space_storage.get_space.return_value = None

        with pytest.raises(SpaceNotFound) as exc:
            self.interactor.update_list(dto, user_id="user_id")

        snapshot.assert_match(repr(exc.value), "space_not_found.txt")
