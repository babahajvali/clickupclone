import pytest
from unittest.mock import create_autospec

from task_management.exceptions.custom_exceptions import (
    EmptyName,
    FolderDeletedException,
    FolderNotFound,
    InvalidOrder,
    ModificationNotAllowed,
    NothingToUpdateFolderException,
    SpaceDeletedException,
    SpaceNotFound,
    UnsupportedVisibilityType,
)
from task_management.exceptions.enums import Role, Visibility
from task_management.interactors.dtos import (
    CreateFolderDTO,
    FolderDTO,
    WorkspaceMemberDTO,
)
from task_management.interactors.spaces.folder_interactor import FolderInteractor
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


class TestFolderInteractor:
    @staticmethod
    def _get_folder_dto(*, order=1, is_deleted=False, is_private=False):
        return FolderDTO(
            folder_id="folder_1",
            name="Folder name",
            description="Folder description",
            space_id="space_1",
            order=order,
            is_deleted=is_deleted,
            created_by="user_1",
            is_private=is_private,
        )

    @staticmethod
    def _get_create_folder_dto():
        return CreateFolderDTO(
            name="Folder name",
            description="Folder description",
            space_id="space_1",
            created_by="user_1",
            is_private=False,
        )

    def _get_interactor(
        self,
        *,
        role: Role = Role.MEMBER,
        space_exists=True,
        space_active=True,
        folder_exists=True,
        folder_active=True,
        folder_order=1,
        space_folder_count=3,
    ):
        folder_storage = create_autospec(FolderStorageInterface)
        space_storage = create_autospec(SpaceStorageInterface)
        workspace_storage = create_autospec(WorkspaceStorageInterface)

        folder_data = self._get_folder_dto(
            order=folder_order, is_deleted=not folder_active
        )
        folder_storage.get_folder.return_value = folder_data if folder_exists else None
        folder_storage.get_folder_space_id.return_value = "space_1"
        folder_storage.get_next_folder_order_in_space.return_value = 2
        folder_storage.get_space_folder_count.return_value = space_folder_count
        folder_storage.create_folder.return_value = folder_data
        folder_storage.update_folder.return_value = folder_data
        folder_storage.update_folder_order.return_value = folder_data
        folder_storage.delete_folder.return_value = folder_data
        folder_storage.update_folder_visibility.return_value = folder_data
        folder_storage.get_space_folders.return_value = [folder_data]

        space_storage.get_space.return_value = (
            type("Space", (), {"is_deleted": not space_active})()
            if space_exists
            else None
        )
        space_storage.get_space_workspace_id.return_value = "workspace_1"

        workspace_storage.get_workspace_member.return_value = make_permission(role)

        interactor = FolderInteractor(
            folder_storage=folder_storage,
            space_storage=space_storage,
            workspace_storage=workspace_storage,
        )
        return interactor

    def test_create_folder_success(self):
        interactor = self._get_interactor()
        dto = self._get_create_folder_dto()

        result = interactor.create_folder(dto)

        assert result.folder_id == "folder_1"
        interactor.folder_storage.get_next_folder_order_in_space.assert_called_once_with(
            space_id="space_1"
        )
        interactor.folder_storage.create_folder.assert_called_once_with(dto, order=2)

    def test_create_folder_empty_name(self):
        interactor = self._get_interactor()
        dto = CreateFolderDTO(
            name=" ",
            description="Folder description",
            space_id="space_1",
            created_by="user_1",
            is_private=False,
        )

        with pytest.raises(EmptyName) as exc:
            interactor.create_folder(dto)

        assert exc.value.name == " "

    def test_create_folder_permission_denied(self):
        interactor = self._get_interactor(role=Role.GUEST)
        dto = self._get_create_folder_dto()

        with pytest.raises(ModificationNotAllowed) as exc:
            interactor.create_folder(dto)

        assert exc.value.user_id == "user_1"

    def test_create_folder_space_not_found(self):
        interactor = self._get_interactor(space_exists=False)
        dto = self._get_create_folder_dto()

        with pytest.raises(SpaceNotFound) as exc:
            interactor.create_folder(dto)

        assert exc.value.space_id == "space_1"

    def test_create_folder_space_inactive(self):
        interactor = self._get_interactor(space_active=False)
        dto = self._get_create_folder_dto()

        with pytest.raises(SpaceDeletedException) as exc:
            interactor.create_folder(dto)

        assert exc.value.space_id == "space_1"

    def test_update_folder_success(self):
        interactor = self._get_interactor()

        result = interactor.update_folder(
            folder_id="folder_1",
            user_id="user_1",
            name="Updated",
            description="Updated description",
        )

        assert result.folder_id == "folder_1"
        interactor.folder_storage.update_folder.assert_called_once_with(
            folder_id="folder_1", name="Updated", description="Updated description"
        )

    def test_update_folder_not_found(self):
        interactor = self._get_interactor(folder_exists=False)

        with pytest.raises(FolderNotFound) as exc:
            interactor.update_folder(
                folder_id="folder_1",
                user_id="user_1",
                name="Updated",
                description=None,
            )

        assert exc.value.folder_id == "folder_1"

    def test_update_folder_inactive(self):
        interactor = self._get_interactor(folder_active=False)

        with pytest.raises(FolderDeletedException) as exc:
            interactor.update_folder(
                folder_id="folder_1",
                user_id="user_1",
                name="Updated",
                description=None,
            )

        assert exc.value.folder_id == "folder_1"

    def test_update_folder_nothing_to_update(self):
        interactor = self._get_interactor()

        with pytest.raises(NothingToUpdateFolderException) as exc:
            interactor.update_folder(
                folder_id="folder_1",
                user_id="user_1",
                name=None,
                description=None,
            )

        assert exc.value.folder_id == "folder_1"

    def test_reorder_folder_success(self):
        interactor = self._get_interactor(folder_order=1)

        result = interactor.reorder_folder(
            space_id="space_1", folder_id="folder_1", user_id="user_1", order=2
        )

        assert result.folder_id == "folder_1"
        interactor.folder_storage.shift_folders_up.assert_called_once_with(
            space_id="space_1", old_order=1, new_order=2
        )
        interactor.folder_storage.update_folder_order.assert_called_once_with(
            folder_id="folder_1", new_order=2
        )

    def test_reorder_folder_same_order_noop(self):
        interactor = self._get_interactor(folder_order=2)

        result = interactor.reorder_folder(
            space_id="space_1", folder_id="folder_1", user_id="user_1", order=2
        )

        assert result.order == 2
        interactor.folder_storage.update_folder_order.assert_not_called()
        interactor.folder_storage.shift_folders_up.assert_not_called()
        interactor.folder_storage.shift_folders_down.assert_not_called()

    def test_reorder_folder_invalid_order_low(self):
        interactor = self._get_interactor(space_folder_count=3)

        with pytest.raises(InvalidOrder) as exc:
            interactor.reorder_folder(
                space_id="space_1", folder_id="folder_1", user_id="user_1", order=0
            )

        assert exc.value.order == 0

    def test_reorder_folder_invalid_order_high(self):
        interactor = self._get_interactor(space_folder_count=3)

        with pytest.raises(InvalidOrder) as exc:
            interactor.reorder_folder(
                space_id="space_1", folder_id="folder_1", user_id="user_1", order=5
            )

        assert exc.value.order == 5

    def test_delete_folder_success(self):
        interactor = self._get_interactor()

        result = interactor.delete_folder(folder_id="folder_1", user_id="user_1")

        assert result.folder_id == "folder_1"
        interactor.folder_storage.delete_folder.assert_called_once_with("folder_1")

    def test_set_folder_visibility_success(self):
        interactor = self._get_interactor()

        result = interactor.set_folder_visibility(
            folder_id="folder_1", user_id="user_1", visibility=Visibility.PRIVATE
        )

        assert result.folder_id == "folder_1"
        interactor.folder_storage.update_folder_visibility.assert_called_once_with(
            folder_id="folder_1", visibility=Visibility.PRIVATE.value
        )

    def test_set_folder_visibility_invalid_type(self):
        interactor = self._get_interactor()

        with pytest.raises(UnsupportedVisibilityType) as exc:
            interactor.set_folder_visibility(
                folder_id="folder_1",
                user_id="user_1",
                visibility=InvalidVisibility,
            )

        assert exc.value.visibility_type == InvalidVisibility.value

    def test_get_space_folders_success(self):
        interactor = self._get_interactor()

        result = interactor.get_space_folders(space_id="space_1")

        assert len(result) == 1
        assert result[0].folder_id == "folder_1"
        interactor.folder_storage.get_space_folders.assert_called_once_with(
            space_ids=["space_1"]
        )
