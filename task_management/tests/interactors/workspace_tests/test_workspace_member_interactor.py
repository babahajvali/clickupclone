import pytest
from unittest.mock import create_autospec

from task_management.exceptions.custom_exceptions import (
    NotAccessToModificationException,
    UnexpectedRoleFoundException
)
from task_management.exceptions.enums import PermissionsEnum, RoleEnum
from task_management.interactors.workspace_interactors.workspace_member_interactors import (
    WorkspaceMemberInteractor
)

from task_management.interactors.storage_interface.workspace_storage_interface import (
    WorkspaceStorageInterface
)
from task_management.interactors.storage_interface.workspace_member_storage_interface import (
    WorkspaceMemberStorageInterface
)
from task_management.interactors.storage_interface.user_storage_interface import (
    UserStorageInterface
)
from task_management.interactors.storage_interface.space_permission_storage_interface import (
    SpacePermissionStorageInterface
)
from task_management.interactors.storage_interface.folder_permission_storage_interface import (
    FolderPermissionStorageInterface
)
from task_management.interactors.storage_interface.list_permission_storage_interface import (
    ListPermissionStorageInterface
)
from task_management.interactors.storage_interface.space_storage_interface import (
    SpaceStorageInterface
)
from task_management.interactors.storage_interface.folder_storage_interface import (
    FolderStorageInterface
)
from task_management.interactors.storage_interface.list_storage_interface import (
    ListStorageInterface
)

from task_management.tests.factories.interactor_factory import (
    AddMemberToWorkspaceDTOFactory,
    WorkspaceMemberDTOFactory
)


class TestWorkspaceMemberInteractor:

    def setup_method(self):
        self.workspace_storage = create_autospec(WorkspaceStorageInterface)
        self.workspace_member_storage = create_autospec(
            WorkspaceMemberStorageInterface)
        self.user_storage = create_autospec(UserStorageInterface)

        self.space_permission_storage = create_autospec(
            SpacePermissionStorageInterface)
        self.folder_permission_storage = create_autospec(
            FolderPermissionStorageInterface)
        self.list_permission_storage = create_autospec(
            ListPermissionStorageInterface)

        self.space_storage = create_autospec(SpaceStorageInterface)
        self.folder_storage = create_autospec(FolderStorageInterface)
        self.list_storage = create_autospec(ListStorageInterface)

        self.interactor = WorkspaceMemberInteractor(
            workspace_member_storage=self.workspace_member_storage,
            workspace_storage=self.workspace_storage,
            user_storage=self.user_storage,
            space_permission_storage=self.space_permission_storage,
            folder_permission_storage=self.folder_permission_storage,
            list_permission_storage=self.list_permission_storage,
            space_storage=self.space_storage,
            folder_storage=self.folder_storage,
            list_storage=self.list_storage
        )

    # ---------- helpers ----------

    def _mock_active_workspace(self, owner_id="admin123"):
        return type("Workspace",(),
            {
                "workspace_id": "workspace123",
                "owner_id": owner_id,
                "is_active": True
            })()

    def _mock_active_user(self):
        return type("User", (), {"is_active": True})()

    def _mock_space(self, space_id="space123"):
        return type("Space", (), {"space_id": space_id})()

    def _mock_folder(self, folder_id="folder123"):
        return type("Folder", (), {"folder_id": folder_id})()

    def _mock_list(self, list_id="list123"):
        return type("List", (), {"list_id": list_id})()


    def test_add_member_to_workspace_success(self, snapshot):
        dto = AddMemberToWorkspaceDTOFactory()
        expected = WorkspaceMemberDTOFactory()

        self.workspace_storage.get_workspace.return_value = (
            self._mock_active_workspace(owner_id=dto.added_by)
        )
        self.user_storage.get_user_data.return_value = self._mock_active_user()
        self.workspace_member_storage.add_member_to_workspace.return_value = expected

        self.space_storage.get_workspace_spaces.return_value = [self._mock_space()]
        self.folder_storage.get_space_folders.return_value = [self._mock_folder()]
        self.list_storage.get_space_lists.return_value = [self._mock_list()]

        result = self.interactor.add_member_to_workspace(dto)

        assert result == expected

        # snapshot.assert_match(repr(result), "add_member_success.txt")

        self.space_permission_storage.create_user_space_permissions.assert_called_once()
        self.folder_permission_storage.create_folder_users_permissions.assert_called_once()
        self.list_permission_storage.create_list_users_permissions.assert_called_once()

    def test_add_member_invalid_role(self, snapshot):
        dto = AddMemberToWorkspaceDTOFactory()
        dto.role = type("Role", (), {"value": "INVALID"})()

        self.workspace_storage.get_workspace.return_value = self._mock_active_workspace()
        self.user_storage.get_user_data.return_value = self._mock_active_user()

        with pytest.raises(UnexpectedRoleFoundException) as exc:
            self.interactor.add_member_to_workspace(dto)

        snapshot.assert_match(repr(exc.value), "add_member_invalid_role.txt")

    def test_add_member_permission_denied(self, snapshot):
        dto = AddMemberToWorkspaceDTOFactory()

        self.workspace_storage.get_workspace.return_value = (
            self._mock_active_workspace(owner_id="someone_else")
        )
        self.user_storage.get_user_data.return_value = self._mock_active_user()

        self.workspace_member_storage.get_workspace_member.return_value = (
            type("WorkspaceMember", (), {"role": RoleEnum.GUEST.value})()
        )

        with pytest.raises(NotAccessToModificationException) as exc:
            self.interactor.add_member_to_workspace(dto)

        snapshot.assert_match(
            repr(exc.value),
            "add_member_permission_denied.txt"
        )


    def test_remove_member_success(self, snapshot):
        expected = WorkspaceMemberDTOFactory()

        self.workspace_storage.get_workspace.return_value = self._mock_active_workspace()
        self.user_storage.get_user_data.return_value = self._mock_active_user()
        self.workspace_member_storage.remove_member_from_workspace.return_value = expected

        self.space_storage.get_workspace_spaces.return_value = [self._mock_space()]
        self.folder_storage.get_space_folders.return_value = [self._mock_folder()]
        self.list_storage.get_space_lists.return_value = [self._mock_list()]

        result = self.interactor.remove_member_from_workspace(
            user_id="user123",
            workspace_id="workspace123",
            removed_by="admin123"
        )
        assert result == expected

        # snapshot.assert_match(repr(result), "remove_member_success.txt")

        self.space_permission_storage.remove_user_permission_for_space.assert_called_once()
        self.folder_permission_storage.remove_user_permission_for_folder.assert_called_once()
        self.list_permission_storage.remove_user_permission_for_list.assert_called_once()


    def test_change_member_role_success(self, snapshot):
        expected = WorkspaceMemberDTOFactory(role=RoleEnum.MEMBER)

        self.workspace_storage.get_workspace.return_value = self._mock_active_workspace()
        self.user_storage.get_user_data.return_value = self._mock_active_user()
        self.workspace_member_storage.update_the_member_role.return_value = expected

        self.space_storage.get_workspace_spaces.return_value = [self._mock_space()]
        self.folder_storage.get_space_folders.return_value = [self._mock_folder()]
        self.list_storage.get_space_lists.return_value = [self._mock_list()]

        result = self.interactor.change_member_role(
            workspace_id="workspace123",
            user_id="user123",
            role=RoleEnum.MEMBER,
            changed_by="admin123"
        )
        assert result == expected

        # snapshot.assert_match(repr(result), "change_role_success.txt")

        self.space_permission_storage.update_user_permission_for_space.assert_called_once()
        self.folder_permission_storage.update_user_permission_for_folder.assert_called_once()
        self.list_permission_storage.update_user_permission_for_list.assert_called_once()

    def test_change_member_role_invalid(self, snapshot):
        self.workspace_storage.get_workspace.return_value = self._mock_active_workspace()
        self.user_storage.get_user_data.return_value = self._mock_active_user()

        with pytest.raises(UnexpectedRoleFoundException) as exc:
            self.interactor.change_member_role(
                workspace_id="workspace123",
                user_id="user123",
                role=type("Role", (), {"value": "INVALID"})(),
                changed_by="admin123"
            )

        snapshot.assert_match(repr(exc.value),"change_role_invalid.txt")
