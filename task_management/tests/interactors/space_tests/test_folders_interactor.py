import pytest
from unittest.mock import create_autospec

from task_management.exceptions.custom_exceptions import *
from task_management.exceptions.enums import Role, Visibility
from task_management.interactors.dtos import (
    CreateFolderDTO,
    FolderDTO,
    WorkspaceMemberDTO,
)
from task_management.interactors.spaces.folder_interactor import \
    FolderInteractor
from task_management.interactors.storage_interfaces import (
    FolderStorageInterface,
    SpaceStorageInterface,
    WorkspaceStorageInterface,
)


class InvalidVisibility:
    value = "INVALID"


def make_permission(role: Role):
    return WorkspaceMemberDTO(
        id=1,
        workspace_id="workspace_1",
        role=role,
        user_id="user_1",
        is_active=True,
        added_by="admin",
    )


def make_folder(order=1, is_deleted=False):
    return FolderDTO(
        folder_id="folder_1",
        name="Folder name",
        description="Folder description",
        space_id="space_1",
        order=order,
        is_deleted=is_deleted,
        created_by="user_1",
        is_private=False,
    )


class TestFolderInteractorSnapshots:

    def _get_interactor(
            self,
            *,
            role=Role.MEMBER,
            space_exists=True,
            space_active=True,
            folder_exists=True,
            folder_active=True,
            folder_order=1,
            space_folder_count=3,
    ):
        self.folder_storage = create_autospec(FolderStorageInterface)
        self.space_storage = create_autospec(SpaceStorageInterface)
        self.workspace_storage = create_autospec(WorkspaceStorageInterface)

        folder = make_folder(order=folder_order, is_deleted=not folder_active)

        self.folder_storage.get_folder.return_value = folder if folder_exists else None
        self.folder_storage.get_space_folder_count.return_value = space_folder_count
        self.folder_storage.get_space_folders.return_value = [folder]
        self.folder_storage.create_folder.return_value = folder
        self.folder_storage.update_folder.return_value = folder
        self.folder_storage.update_folder_order.return_value = folder
        self.folder_storage.delete_folder.return_value = folder
        self.folder_storage.update_folder_visibility.return_value = folder

        self.space_storage.get_space.return_value = (
            type("Space", (), {"is_deleted": not space_active})()
            if space_exists
            else None
        )

        self.workspace_storage.get_workspace_member.return_value = make_permission(
            role)

        self.interactor = FolderInteractor(
            folder_storage=self.folder_storage,
            space_storage=self.space_storage,
            workspace_storage=self.workspace_storage,
        )

    def test_create_folder_success(self, snapshot):
        self._get_interactor()

        dto = CreateFolderDTO(
            name="Folder name",
            description="Folder description",
            space_id="space_1",
            created_by="user_1",
            is_private=False,
        )

        result = self.interactor.create_folder(dto)

        snapshot.assert_match(repr(result), "create_folder_success.txt")

    def test_create_folder_empty_name(self, snapshot):
        self._get_interactor()

        dto = CreateFolderDTO(
            name=" ",
            description="Folder description",
            space_id="space_1",
            created_by="user_1",
            is_private=False,
        )

        with pytest.raises(EmptyFolderName) as exc:
            self.interactor.create_folder(dto)

        snapshot.assert_match(repr(exc.value), "create_folder_empty_name.txt")

    def test_create_folder_space_not_found(self, snapshot):
        self._get_interactor(space_exists=False)

        dto = CreateFolderDTO(
            name="Folder name",
            description="Folder description",
            space_id="space_1",
            created_by="user_1",
            is_private=False,
        )

        with pytest.raises(SpaceNotFound) as exc:
            self.interactor.create_folder(dto)

        snapshot.assert_match(repr(exc.value), "space_not_found.txt")

    def test_create_folder_permission_denied(self, snapshot):
        self._get_interactor(role=Role.GUEST)

        dto = CreateFolderDTO(
            name="Folder name",
            description="Folder description",
            space_id="space_1",
            created_by="user_1",
            is_private=False,
        )

        with pytest.raises(ModificationNotAllowed) as exc:
            self.interactor.create_folder(dto)

        snapshot.assert_match(repr(exc.value),
                              "create_folder_permission_denied.txt")

    def test_create_folder_space_inactive(self, snapshot):
        self._get_interactor(space_active=False)

        dto = CreateFolderDTO(
            name="Folder name",
            description="Folder description",
            space_id="space_1",
            created_by="user_1",
            is_private=False,
        )

        with pytest.raises(DeletedSpaceFound) as exc:
            self.interactor.create_folder(dto)

        snapshot.assert_match(repr(exc.value),
                              "create_folder_space_inactive.txt")

    def test_update_folder_not_found(self, snapshot):
        self._get_interactor(folder_exists=False)

        with pytest.raises(FolderNotFound) as exc:
            self.interactor.update_folder(
                folder_id="folder_1",
                user_id="user_1",
                name="Updated",
                description=None,
            )

        snapshot.assert_match(repr(exc.value), "update_folder_not_found.txt")

    def test_update_folder_inactive(self, snapshot):
        self._get_interactor(folder_active=False)

        with pytest.raises(DeletedFolderException) as exc:
            self.interactor.update_folder(
                folder_id="folder_1",
                user_id="user_1",
                name="Updated",
                description=None,
            )

        snapshot.assert_match(repr(exc.value), "update_folder_inactive.txt")

    def test_update_folder_success(self, snapshot):
        self._get_interactor()

        result = self.interactor.update_folder(
            folder_id="folder_1",
            user_id="user_1",
            name="Updated",
            description="Updated description",
        )

        snapshot.assert_match(repr(result), "update_folder_success.txt")

    def test_update_folder_nothing_to_update(self, snapshot):
        self._get_interactor()

        with pytest.raises(NothingToUpdateFolderException) as exc:
            self.interactor.update_folder(
                folder_id="folder_1",
                user_id="user_1",
                name=None,
                description=None,
            )

        snapshot.assert_match(repr(exc.value),
                              "update_folder_nothing_to_update.txt")

    def test_reorder_folder_invalid_low(self, snapshot):
        self._get_interactor(space_folder_count=3)

        with pytest.raises(InvalidOrder) as exc:
            self.interactor.reorder_folder(
                space_id="space_1",
                folder_id="folder_1",
                user_id="user_1",
                order=0,
            )

        snapshot.assert_match(repr(exc.value), "reorder_invalid_low.txt")

    def test_reorder_folder_success(self, snapshot):
        self._get_interactor(folder_order=1)

        result = self.interactor.reorder_folder(
            space_id="space_1",
            folder_id="folder_1",
            user_id="user_1",
            order=2,
        )

        snapshot.assert_match(repr(result), "reorder_folder_success.txt")

    def test_reorder_folder_same_order_noop(self, snapshot):
        self._get_interactor(folder_order=2)

        result = self.interactor.reorder_folder(
            space_id="space_1",
            folder_id="folder_1",
            user_id="user_1",
            order=2,
        )

        snapshot.assert_match(repr(result), "reorder_folder_same_order.txt")

    def test_reorder_folder_invalid_order_high(self, snapshot):
        self._get_interactor(space_folder_count=3)

        with pytest.raises(InvalidOrder) as exc:
            self.interactor.reorder_folder(
                space_id="space_1",
                folder_id="folder_1",
                user_id="user_1",
                order=5,
            )

        snapshot.assert_match(repr(exc.value), "reorder_invalid_high.txt")

    def test_delete_folder_success(self, snapshot):
        self._get_interactor()

        result = self.interactor.delete_folder(
            folder_id="folder_1",
            user_id="user_1",
        )

        snapshot.assert_match(repr(result), "delete_folder_success.txt")

    def test_invalid_visibility(self, snapshot):
        self._get_interactor()

        with pytest.raises(UnsupportedVisibilityType) as exc:
            self.interactor.set_folder_visibility(
                folder_id="folder_1",
                user_id="user_1",
                visibility=InvalidVisibility,
            )

        snapshot.assert_match(repr(exc.value), "invalid_visibility.txt")

    def test_set_folder_visibility_success(self, snapshot):
        self._get_interactor()

        result = self.interactor.set_folder_visibility(
            folder_id="folder_1",
            user_id="user_1",
            visibility=Visibility.PRIVATE,
        )

        snapshot.assert_match(repr(result), "set_visibility_success.txt")

    def test_get_space_folders_success(self, snapshot):
        self._get_interactor()

        result = self.interactor.get_space_folders(space_id="space_1")

        snapshot.assert_match(repr(result), "get_space_folders.txt")
