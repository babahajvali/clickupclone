import pytest
from unittest.mock import create_autospec

from task_management.exceptions.custom_exceptions import (
    EmptyName,
    InactiveList,
    ListNotFound,
    ModificationNotAllowed,
    NothingToUpdateList,
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


class TestUpdateList:
    @staticmethod
    def _get_list_dto():
        return ListDTO(
            list_id="list_1",
            name="List name",
            description="List description",
            space_id="space_1",
            is_active=True,
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
        list_storage.update_list.return_value = list_data

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

    def test_update_list_success(self, snapshot):
        interactor = self._get_interactor()

        result = interactor.update_list(
            list_id="list_1",
            user_id="user_id",
            name="Updated name",
            description="Updated description",
        )

        snapshot.assert_match(
            repr(result),
            "test_update_list_success.txt",
        )

    def test_update_list_nothing_to_update(self, snapshot):
        interactor = self._get_interactor()

        with pytest.raises(NothingToUpdateList) as exc:
            interactor.update_list(
                list_id="list_1",
                user_id="user_id",
                name=None,
                description=None,
            )

        snapshot.assert_match(
            repr(exc.value.list_id),
            "test_update_list_nothing_to_update.txt",
        )

    def test_update_list_empty_name(self, snapshot):
        interactor = self._get_interactor()

        with pytest.raises(EmptyName) as exc:
            interactor.update_list(
                list_id="list_1",
                user_id="user_id",
                name=" ",
                description=None,
            )

        snapshot.assert_match(
            repr(exc.value.name),
            "test_update_list_empty_name.txt",
        )

    def test_update_list_not_found(self, snapshot):
        interactor = self._get_interactor(list_data=None)
        interactor.list_storage.get_list.return_value = None

        with pytest.raises(ListNotFound) as exc:
            interactor.update_list(
                list_id="list_1",
                user_id="user_id",
                name="Updated name",
                description=None,
            )

        snapshot.assert_match(
            repr(exc.value.list_id),
            "test_update_list_not_found.txt",
        )

    def test_update_list_inactive(self, snapshot):
        list_data = self._get_list_dto()
        list_data.is_active = False
        interactor = self._get_interactor(list_data=list_data)

        with pytest.raises(InactiveList) as exc:
            interactor.update_list(
                list_id="list_1",
                user_id="user_id",
                name="Updated name",
                description=None,
            )

        snapshot.assert_match(
            repr(exc.value.list_id),
            "test_update_list_inactive.txt",
        )

    def test_update_list_permission_denied(self, snapshot):
        interactor = self._get_interactor(role=Role.GUEST)

        with pytest.raises(ModificationNotAllowed) as exc:
            interactor.update_list(
                list_id="list_1",
                user_id="user_id",
                name="Updated name",
                description=None,
            )

        snapshot.assert_match(
            repr(exc.value.user_id),
            "test_update_list_permission_denied.txt",
        )
