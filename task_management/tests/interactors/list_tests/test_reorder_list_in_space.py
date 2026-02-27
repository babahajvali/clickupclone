from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import (
    DeletedSpaceFound,
    InvalidOrder,
    DeletedListFound,
    ListNotFound,
    ModificationNotAllowed,
    SpaceNotFound,
)
from task_management.exceptions.enums import Role
from task_management.interactors.dtos import ListDTO, WorkspaceMemberDTO
from task_management.interactors.lists.reorder_list_in_space_interactor import (
    ReorderListInSpaceInteractor,
)
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


class TestReorderListInSpace:
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

    def _get_interactor(
        self,
        *,
        role: Role = Role.MEMBER,
        list_data=None,
        space_exists=True,
        space_active=True,
        space_lists_count=3,
    ):
        list_storage = create_autospec(ListStorageInterface)
        folder_storage = create_autospec(FolderStorageInterface)
        space_storage = create_autospec(SpaceStorageInterface)
        workspace_storage = create_autospec(WorkspaceStorageInterface)

        if list_data is None:
            list_data = self._get_list_dto()

        list_storage.get_list.return_value = list_data
        list_storage.get_space_lists_count.return_value = space_lists_count
        list_storage.update_list_order_in_space.return_value = list_data

        space_storage.get_space.return_value = (
            type("Space", (), {"is_deleted": not space_active})()
            if space_exists
            else None
        )
        space_storage.get_space_workspace_id.return_value = "workspace_id1"

        workspace_storage.get_workspace_member.return_value = make_permission(
            role
        )

        return ReorderListInSpaceInteractor(
            list_storage=list_storage,
            folder_storage=folder_storage,
            space_storage=space_storage,
            workspace_storage=workspace_storage,
        )

    def test_reorder_list_in_space_success(self):
        interactor = self._get_interactor()

        result = interactor.reorder_list_in_space(
            list_id="list_1",
            space_id="space_1",
            order=2,
            user_id="user_id",
        )

        assert result.list_id == "list_1"
        interactor.list_storage.shift_lists_down_in_space.assert_called_once_with(
            space_id="space_1", old_order=1, new_order=2
        )
        interactor.list_storage.update_list_order_in_space.assert_called_once_with(
            space_id="space_1", list_id="list_1", order=2
        )

    def test_reorder_list_in_space_same_order_noop(self):
        interactor = self._get_interactor()

        result = interactor.reorder_list_in_space(
            list_id="list_1",
            space_id="space_1",
            order=1,
            user_id="user_id",
        )

        assert result.order == 1
        interactor.list_storage.update_list_order_in_space.assert_not_called()
        interactor.list_storage.shift_lists_down_in_space.assert_not_called()
        interactor.list_storage.shift_lists_up_in_space.assert_not_called()

    def test_reorder_list_in_space_invalid_order_low(self):
        interactor = self._get_interactor(space_lists_count=3)

        with pytest.raises(InvalidOrder) as exc:
            interactor.reorder_list_in_space(
                list_id="list_1",
                space_id="space_1",
                order=0,
                user_id="user_id",
            )

        assert exc.value.order == 0

    def test_reorder_list_in_space_invalid_order_high(self):
        interactor = self._get_interactor(space_lists_count=3)

        with pytest.raises(InvalidOrder) as exc:
            interactor.reorder_list_in_space(
                list_id="list_1",
                space_id="space_1",
                order=5,
                user_id="user_id",
            )

        assert exc.value.order == 5

    def test_reorder_list_in_space_list_not_found(self):
        interactor = self._get_interactor(list_data=None)
        interactor.list_storage.get_list.return_value = None

        with pytest.raises(ListNotFound) as exc:
            interactor.reorder_list_in_space(
                list_id="list_1",
                space_id="space_1",
                order=1,
                user_id="user_id",
            )

        assert exc.value.list_id == "list_1"

    def test_reorder_list_in_space_list_inactive(self):
        list_data = self._get_list_dto()
        list_data.is_deleted = True
        interactor = self._get_interactor(list_data=list_data)

        with pytest.raises(DeletedListFound) as exc:
            interactor.reorder_list_in_space(
                list_id="list_1",
                space_id="space_1",
                order=1,
                user_id="user_id",
            )

        assert exc.value.list_id == "list_1"

    def test_reorder_list_in_space_space_not_found(self):
        interactor = self._get_interactor(space_exists=False)

        with pytest.raises(SpaceNotFound) as exc:
            interactor.reorder_list_in_space(
                list_id="list_1",
                space_id="space_1",
                order=1,
                user_id="user_id",
            )

        assert exc.value.space_id == "space_1"

    def test_reorder_list_in_space_space_inactive(self):
        interactor = self._get_interactor(space_active=False)

        with pytest.raises(DeletedSpaceFound) as exc:
            interactor.reorder_list_in_space(
                list_id="list_1",
                space_id="space_1",
                order=1,
                user_id="user_id",
            )

        assert exc.value.space_id == "space_1"

    def test_reorder_list_in_space_permission_denied(self):
        interactor = self._get_interactor(role=Role.GUEST)

        with pytest.raises(ModificationNotAllowed) as exc:
            interactor.reorder_list_in_space(
                list_id="list_1",
                space_id="space_1",
                order=1,
                user_id="user_id",
            )

        assert exc.value.user_id == "user_id"
