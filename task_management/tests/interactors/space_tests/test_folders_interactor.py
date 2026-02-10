import pytest
from unittest.mock import create_autospec

from task_management.exceptions.enums import Permissions, Visibility, Role
from task_management.interactors.dtos import UserSpacePermissionDTO, \
    UserFolderPermissionDTO, WorkspaceMemberDTO
from task_management.interactors.space_interactors.folders_interactor import \
    FolderInteractor
from task_management.interactors.storage_interface.folder_storage_interface import \
    FolderStorageInterface
from task_management.interactors.storage_interface.space_storage_interface import \
    SpaceStorageInterface
from task_management.interactors.storage_interface.space_permission_storage_interface import (
    SpacePermissionStorageInterface
)
from task_management.interactors.storage_interface.folder_permission_storage_interface import (
    FolderPermissionStorageInterface
)
from task_management.exceptions.custom_exceptions import (
    ModificationNotAllowedException,
    InactiveSpaceException,
    FolderNotFoundException,
    InactiveFolderException,
)
from task_management.interactors.storage_interface.workspace_member_storage_interface import \
    WorkspaceMemberStorageInterface
from task_management.tests.factories.interactor_factory import (
    CreateFolderDTOFactory,
    UpdateFolderDTOFactory,
    FolderDTOFactory,
)


def make_permission(role: Role):
    return WorkspaceMemberDTO(
        id=1,
        workspace_id="workspace_id1",
        role=role,
        user_id="user_id",
        is_active=True,
        added_by="admin"
    )



class TestFolderInteractor:

    def setup_method(self):
        self.folder_storage = create_autospec(FolderStorageInterface)
        self.space_storage = create_autospec(SpaceStorageInterface)
        self.workspace_member_storage = create_autospec(
            WorkspaceMemberStorageInterface)
        self.folder_permission_storage = create_autospec(
            FolderPermissionStorageInterface)

        self.interactor = FolderInteractor(
            folder_storage=self.folder_storage,
            space_storage=self.space_storage,
            folder_permission_storage=self.folder_permission_storage,
            workspace_member_storage=self.workspace_member_storage
        )

    def test_create_folder_success(self, snapshot):
        dto = CreateFolderDTOFactory()
        expected = FolderDTOFactory()

        self.workspace_member_storage.get_workspace_member.return_value = make_permission(
            Role.MEMBER
        )
        self.space_storage.get_space.return_value = type(
            "Space", (), {"is_active": True}
        )()
        self.folder_storage.create_folder.return_value = expected

        result = self.interactor.create_folder(dto)

        snapshot.assert_match(
            repr(result),
            "create_folder_success.txt"
        )

    def test_create_folder_permission_denied(self, snapshot):
        dto = CreateFolderDTOFactory()

        self.workspace_member_storage.get_workspace_member.return_value = make_permission(
            Role.GUEST
        )

        with pytest.raises(ModificationNotAllowedException) as exc:
            self.interactor.create_folder(dto)

        snapshot.assert_match(
            repr(exc.value.user_id),
            "create_folder_permission_denied.txt"
        )

    def test_create_folder_inactive_space(self, snapshot):
        dto = CreateFolderDTOFactory()

        self.workspace_member_storage.get_workspace_member.return_value = make_permission(
            Role.MEMBER
        )
        self.space_storage.get_space.return_value = type(
            "Space", (), {"is_active": False}
        )()

        with pytest.raises(InactiveSpaceException) as exc:
            self.interactor.create_folder(dto)

        snapshot.assert_match(
            repr(exc.value.space_id),
            "create_folder_inactive_space.txt"
        )

    def test_update_folder_success(self, snapshot):
        dto = UpdateFolderDTOFactory()
        expected = FolderDTOFactory()

        self.workspace_member_storage.get_workspace_member.return_value = make_permission(
            Role.MEMBER
        )
        self.folder_storage.get_folder.return_value = type(
            "Folder", (), {"is_active": True,
                           "space_id": "space_id", }
        )()
        self.space_storage.get_space.return_value = type(
            "Space", (), {"is_active": True}
        )()
        self.folder_storage.update_folder.return_value = expected

        result = self.interactor.update_folder(dto, user_id="user_id1")

        snapshot.assert_match(
            repr(result),
            "update_folder_success.txt"
        )

    def test_update_folder_permission_denied(self, snapshot):
        dto = UpdateFolderDTOFactory()

        self.workspace_member_storage.get_workspace_member.return_value = make_permission(
            Role.GUEST
        )

        with pytest.raises(ModificationNotAllowedException) as exc:
            self.interactor.update_folder(dto, user_id="user_id1")

        snapshot.assert_match(
            repr(exc.value.user_id),
            "update_folder_permission_denied.txt"
        )

    def test_update_folder_not_found(self, snapshot):
        dto = UpdateFolderDTOFactory()

        self.workspace_member_storage.get_workspace_member.return_value = make_permission(
            Role.MEMBER
        )
        self.folder_storage.get_folder.return_value = None

        with pytest.raises(FolderNotFoundException) as exc:
            self.interactor.update_folder(dto, user_id="user_id1")

        snapshot.assert_match(
            repr(exc.value.folder_id),
            "update_folder_not_found.txt"
        )

    def test_remove_folder_success(self, snapshot):
        folder_id = "folder_1"
        user_id = "user_1"
        expected = FolderDTOFactory(is_active=False)

        self.workspace_member_storage.get_workspace_member.return_value = make_permission(
            Role.MEMBER
        )
        self.folder_storage.get_folder.return_value = type(
            "Folder", (), {"is_active": True}
        )()
        self.folder_storage.remove_folder.return_value = expected

        result = self.interactor.remove_folder(folder_id, user_id)

        snapshot.assert_match(
            repr(result),
            "remove_folder_success.txt"
        )

    def test_remove_folder_not_found(self, snapshot):
        folder_id = "folder_1"
        user_id = "user_1"

        self.workspace_member_storage.get_workspace_member.return_value = make_permission(
            Role.MEMBER
        )
        self.folder_storage.get_folder.return_value = None

        with pytest.raises(FolderNotFoundException) as exc:
            self.interactor.remove_folder(folder_id, user_id)

        snapshot.assert_match(
            repr(exc.value.folder_id),
            "remove_folder_not_found.txt"
        )

    def test_remove_folder_inactive(self, snapshot):
        folder_id = "folder_1"
        user_id = "user_1"

        self.workspace_member_storage.get_workspace_member.return_value = make_permission(
            Role.MEMBER
        )
        self.folder_storage.get_folder.return_value = type(
            "Folder", (), {"is_active": False}
        )()

        with pytest.raises(InactiveFolderException) as exc:
            self.interactor.remove_folder(folder_id, user_id)

        snapshot.assert_match(
            repr(exc.value.folder_id),
            "remove_folder_inactive.txt"
        )

    def test_make_folder_private_success(self, snapshot):
        folder_id = "folder_1"
        user_id = "user_1"
        expected = FolderDTOFactory(is_private=True)

        self.workspace_member_storage.get_workspace_member.return_value = make_permission(
            Role.MEMBER
        )
        self.folder_storage.get_folder.return_value = type(
            "Folder", (), {"is_active": True}
        )()
        self.folder_storage.set_folder_private.return_value = expected

        result = self.interactor.set_folder_visibility(folder_id, user_id,
                                                       Visibility.PRIVATE)

        snapshot.assert_match(
            repr(result),
            "make_folder_private_success.txt"
        )

    def test_make_folder_public_inactive(self, snapshot):
        folder_id = "folder_1"
        user_id = "user_1"

        self.workspace_member_storage.get_workspace_member.return_value = make_permission(
            Role.MEMBER
        )
        self.folder_storage.get_folder.return_value = type(
            "Folder", (), {"is_active": False}
        )()

        with pytest.raises(InactiveFolderException) as exc:
            self.interactor.set_folder_visibility(folder_id, user_id,
                                                  Visibility.PUBLIC)

        snapshot.assert_match(
            repr(exc.value.folder_id),
            "make_folder_public_inactive.txt"
        )
