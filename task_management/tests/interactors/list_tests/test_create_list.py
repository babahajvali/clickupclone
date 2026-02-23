import pytest
from unittest.mock import create_autospec

from task_management.exceptions.custom_exceptions import (
    EmptyName,
    FolderNotFound,
    InactiveFolder,
    InactiveSpace,
    ModificationNotAllowed,
    SpaceNotFound,
)
from task_management.exceptions.enums import Role
from task_management.interactors.dtos import CreateListDTO, ListDTO, \
    WorkspaceMemberDTO
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


class TestCreateList:
    @staticmethod
    def _get_list_dto(*, is_private=False, folder_id=None):
        return ListDTO(
            list_id="list_1",
            name="List name",
            description="List description",
            space_id="space_1",
            is_active=True,
            order=1,
            is_private=is_private,
            created_by="user_id",
            folder_id=folder_id,
        )

    def _get_interactor(
            self,
            *,
            space_active=True,
            folder_active=True,
            folder_exists=True,
            role: Role = Role.MEMBER,
    ):
        list_storage = create_autospec(ListStorageInterface)
        folder_storage = create_autospec(FolderStorageInterface)
        space_storage = create_autospec(SpaceStorageInterface)
        workspace_storage = create_autospec(WorkspaceStorageInterface)

        space_storage.get_space.return_value = (
            type("Space", (), {"is_active": space_active})()
            if space_active is not None else None
        )
        folder_storage.get_folder.return_value = (
            type("Folder", (), {"is_active": folder_active})()
            if folder_exists else None
        )

        list_storage.get_active_lists_last_order_in_space.return_value = 1
        list_storage.get_active_lists_last_order_in_folder.return_value = 1
        list_storage.create_list.return_value = self._get_list_dto(
            folder_id="folder_1"
        )

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

    def test_create_list_success(self, snapshot):
        interactor = self._get_interactor()

        dto = CreateListDTO(
            name="List name",
            description="List description",
            space_id="space_1",
            created_by="user_id",
            is_private=False,
            folder_id="folder_1",
        )

        result = interactor.create_list(dto)

        snapshot.assert_match(
            repr(result),
            "test_create_list_success.txt",
        )

    def test_create_list_empty_name(self, snapshot):
        interactor = self._get_interactor()

        dto = CreateListDTO(
            name=" ",
            description="List description",
            space_id="space_1",
            created_by="user_id",
            is_private=False,
            folder_id=None,
        )

        with pytest.raises(EmptyName) as exc:
            interactor.create_list(dto)

        snapshot.assert_match(
            repr(exc.value.name),
            "test_create_list_empty_name.txt",
        )

    def test_create_list_space_not_found(self, snapshot):
        interactor = self._get_interactor(space_active=None)

        dto = CreateListDTO(
            name="List name",
            description="List description",
            space_id="space_1",
            created_by="user_id",
            is_private=False,
            folder_id=None,
        )

        with pytest.raises(SpaceNotFound) as exc:
            interactor.create_list(dto)

        snapshot.assert_match(
            repr(exc.value.space_id),
            "test_create_list_space_not_found.txt",
        )

    def test_create_list_space_inactive(self, snapshot):
        interactor = self._get_interactor(space_active=False)

        dto = CreateListDTO(
            name="List name",
            description="List description",
            space_id="space_1",
            created_by="user_id",
            is_private=False,
            folder_id=None,
        )

        with pytest.raises(InactiveSpace) as exc:
            interactor.create_list(dto)

        snapshot.assert_match(
            repr(exc.value.space_id),
            "test_create_list_space_inactive.txt",
        )

    def test_create_list_folder_not_found(self, snapshot):
        interactor = self._get_interactor(folder_exists=False)

        dto = CreateListDTO(
            name="List name",
            description="List description",
            space_id="space_1",
            created_by="user_id",
            is_private=False,
            folder_id="folder_1",
        )

        with pytest.raises(FolderNotFound) as exc:
            interactor.create_list(dto)

        snapshot.assert_match(
            repr(exc.value.folder_id),
            "test_create_list_folder_not_found.txt",
        )

    def test_create_list_folder_inactive(self, snapshot):
        interactor = self._get_interactor(folder_active=False)

        dto = CreateListDTO(
            name="List name",
            description="List description",
            space_id="space_1",
            created_by="user_id",
            is_private=False,
            folder_id="folder_1",
        )

        with pytest.raises(InactiveFolder) as exc:
            interactor.create_list(dto)

        snapshot.assert_match(
            repr(exc.value.folder_id),
            "test_create_list_folder_inactive.txt",
        )

    def test_create_list_permission_denied(self, snapshot):
        interactor = self._get_interactor(role=Role.GUEST)

        dto = CreateListDTO(
            name="List name",
            description="List description",
            space_id="space_1",
            created_by="user_id",
            is_private=False,
            folder_id=None,
        )

        with pytest.raises(ModificationNotAllowed) as exc:
            interactor.create_list(dto)

        snapshot.assert_match(
            repr(exc.value.user_id),
            "test_create_list_permission_denied.txt",
        )
