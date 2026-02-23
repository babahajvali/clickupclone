import pytest
from unittest.mock import create_autospec

from task_management.exceptions.custom_exceptions import (
    ListDeletedException,
    ListNotFound,
    ModificationNotAllowed,
)
from task_management.exceptions.enums import Role
from task_management.interactors.dtos import ListDTO, WorkspaceMemberDTO
from task_management.interactors.lists.list_interactor import ListInteractor
from task_management.interactors.storage_interfaces import (
    ListStorageInterface,
    FolderStorageInterface,
    SpaceStorageInterface,
    WorkspaceStorageInterface,
)


def make_permission(role: Role):
    return WorkspaceMemberDTO(
        id=1,
        workspace_id="workspace_id1",
        role=role,
        user_id="user_id",
        is_active=True,
        added_by="admin",
    )


class TestRemoveList:
    @staticmethod
    def _get_list_dto():
        return ListDTO(
            list_id="list_1",
            name="List name",
            description="List description",
            space_id="space_1",
            is_deleted=False,
            order=1,
            is_private=False,
            created_by="user_id",
            folder_id=None,
        )

    def _get_interactor(self, *, role: Role = Role.MEMBER, list_data=None):
        list_storage = create_autospec(ListStorageInterface)
        folder_storage = create_autospec(FolderStorageInterface)
        space_storage = create_autospec(SpaceStorageInterface)
        workspace_storage = create_autospec(WorkspaceStorageInterface)

        if list_data is None:
            list_data = self._get_list_dto()

        list_storage.get_list.return_value = list_data
        list_storage.get_list_space_id.return_value = "space_1"
        list_storage.delete_list.return_value = list_data

        space_storage.get_space_workspace_id.return_value = "workspace_id1"
        workspace_storage.get_workspace_member.return_value = make_permission(
            role
        )

        return ListInteractor(
            list_storage=list_storage,
            folder_storage=folder_storage,
            space_storage=space_storage,
            workspace_storage=workspace_storage,
        )

    def test_remove_list_success(self):
        interactor = self._get_interactor()

        result = interactor.delete_list(list_id="list_1", user_id="user_id")

        assert result.list_id == "list_1"
        interactor.list_storage.delete_list.assert_called_once_with(list_id="list_1")

    def test_remove_list_not_found(self):
        interactor = self._get_interactor(list_data=None)
        interactor.list_storage.get_list.return_value = None

        with pytest.raises(ListNotFound) as exc:
            interactor.delete_list(list_id="list_1", user_id="user_id")

        assert exc.value.list_id == "list_1"

    def test_remove_list_inactive(self):
        list_data = self._get_list_dto()
        list_data.is_deleted = True
        interactor = self._get_interactor(list_data=list_data)

        with pytest.raises(ListDeletedException) as exc:
            interactor.delete_list(list_id="list_1", user_id="user_id")

        assert exc.value.list_id == "list_1"

    def test_remove_list_permission_denied(self):
        interactor = self._get_interactor(role=Role.GUEST)

        with pytest.raises(ModificationNotAllowed) as exc:
            interactor.delete_list(list_id="list_1", user_id="user_id")

        assert exc.value.user_id == "user_id"
