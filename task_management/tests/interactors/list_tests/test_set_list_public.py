import pytest
from unittest.mock import create_autospec

from task_management.exceptions.custom_exceptions import (
    InactiveList,
    ListNotFound,
    ModificationNotAllowed,
)
from task_management.exceptions.enums import Role, Visibility
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


class TestSetListPublic:
    @staticmethod
    def _get_list_dto(is_private=False):
        return ListDTO(
            list_id="list_1",
            name="List name",
            description="List description",
            space_id="space_1",
            is_active=True,
            order=1,
            is_private=is_private,
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
        list_storage.make_list_public.return_value = list_data

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

    def test_set_list_public_success(self, snapshot):
        interactor = self._get_interactor()

        result = interactor.set_list_visibility(
            list_id="list_1",
            visibility=Visibility.PUBLIC,
            user_id="user_id",
        )

        snapshot.assert_match(
            repr(result),
            "test_set_list_public_success.txt",
        )

    def test_set_list_public_not_found(self, snapshot):
        interactor = self._get_interactor(list_data=None)
        interactor.list_storage.get_list.return_value = None

        with pytest.raises(ListNotFound) as exc:
            interactor.set_list_visibility(
                list_id="list_1",
                visibility=Visibility.PUBLIC,
                user_id="user_id",
            )

        snapshot.assert_match(
            repr(exc.value.list_id),
            "test_set_list_public_not_found.txt",
        )

    def test_set_list_public_inactive(self, snapshot):
        list_data = self._get_list_dto()
        list_data.is_active = False
        interactor = self._get_interactor(list_data=list_data)

        with pytest.raises(InactiveList) as exc:
            interactor.set_list_visibility(
                list_id="list_1",
                visibility=Visibility.PUBLIC,
                user_id="user_id",
            )

        snapshot.assert_match(
            repr(exc.value.list_id),
            "test_set_list_public_inactive.txt",
        )

    def test_set_list_public_permission_denied(self, snapshot):
        interactor = self._get_interactor(role=Role.GUEST)

        with pytest.raises(ModificationNotAllowed) as exc:
            interactor.set_list_visibility(
                list_id="list_1",
                visibility=Visibility.PUBLIC,
                user_id="user_id",
            )

        snapshot.assert_match(
            repr(exc.value.user_id),
            "test_set_list_public_permission_denied.txt",
        )
