from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import (
    UnexpectedRole,
    ModificationNotAllowed, InactiveUser, DeletedWorkspaceFound,
)
from task_management.exceptions.enums import Role
from task_management.interactors.storage_interfaces.user_storage_interface import (
    UserStorageInterface
)
from task_management.interactors.storage_interfaces.workspace_storage_interface import (
    WorkspaceStorageInterface
)
from task_management.interactors.workspaces.add_workspace_member_interactor import (
    AddWorkspaceMemberInteractor
)
from task_management.tests.factories.interactor_factory import (
    AddMemberToWorkspaceDTOFactory,
    WorkspaceMemberDTOFactory
)


class TestAddWorkspaceMemberInteractor:

    def setup_method(self):
        self.workspace_storage = create_autospec(WorkspaceStorageInterface)
        self.user_storage = create_autospec(UserStorageInterface)

        self.interactor = AddWorkspaceMemberInteractor(
            workspace_storage=self.workspace_storage,
            user_storage=self.user_storage,
        )

    @staticmethod
    def _mock_active_workspace(owner_id="admin123"):
        return type("Workspace", (), {
            "workspace_id": "workspace123",
            "user_id": owner_id,
            "is_deleted": False
        })()

    @staticmethod
    def _mock_deleted_workspace():
        return type("Workspace", (), {
            "workspace_id": "workspace123",
            "user_id": "admin123",
            "is_deleted": True
        })()

    @staticmethod
    def _mock_active_user():
        return type("User", (), {"is_active": True})()

    @staticmethod
    def _mock_inactive_user():
        return type("User", (), {"is_active": False})()

    def test_add_member_to_workspace_success(self):
        dto = AddMemberToWorkspaceDTOFactory()
        expected = WorkspaceMemberDTOFactory()

        self.workspace_storage.get_workspace.return_value = (
            self._mock_active_workspace(owner_id=dto.added_by)
        )
        self.workspace_storage.get_workspace_member.return_value = type(
            "WorkspaceMember", (), {"role": Role.ADMIN, "is_active": True}
        )()
        self.user_storage.get_user_data.return_value = self._mock_active_user()
        self.workspace_storage.add_member_to_workspace.return_value = expected

        result = self.interactor.add_member_to_workspace(dto)

        assert result == expected
        self.workspace_storage.add_member_to_workspace.assert_called_once_with(
            workspace_member_data=dto
        )

    def test_add_member_invalid_role(self, snapshot):
        dto = AddMemberToWorkspaceDTOFactory()
        dto.role = type("Role", (), {"value": "INVALID"})()

        with pytest.raises(UnexpectedRole) as exc:
            self.interactor.add_member_to_workspace(dto)

        snapshot.assert_match(
            repr(exc.value),
            "add_workspace_member_invalid_role.txt"
        )

    def test_add_member_workspace_deleted(self, snapshot):
        dto = AddMemberToWorkspaceDTOFactory()

        self.workspace_storage.get_workspace.return_value = (
            self._mock_deleted_workspace()
        )

        with pytest.raises(DeletedWorkspaceFound) as exc:
            self.interactor.add_member_to_workspace(dto)

        snapshot.assert_match(
            repr(exc.value),
            "add_workspace_member_workspace_deleted.txt"
        )

    def test_add_member_user_inactive(self, snapshot):
        dto = AddMemberToWorkspaceDTOFactory()

        self.workspace_storage.get_workspace.return_value = (
            self._mock_active_workspace(owner_id=dto.added_by)
        )
        self.workspace_storage.get_workspace_member.return_value = type(
            "WorkspaceMember", (), {"role": Role.ADMIN, "is_active": True}
        )()
        self.user_storage.get_user_data.return_value = self._mock_inactive_user()

        with pytest.raises(InactiveUser) as exc:
            self.interactor.add_member_to_workspace(dto)

        snapshot.assert_match(
            repr(exc.value),
            "add_workspace_member_user_inactive.txt"
        )

    def test_add_member_no_edit_access(self, snapshot):
        dto = AddMemberToWorkspaceDTOFactory()

        self.workspace_storage.get_workspace.return_value = (
            self._mock_active_workspace(owner_id="someone_else")
        )
        self.workspace_storage.get_workspace_member.return_value = type(
            "WorkspaceMember", (), {"role": Role.GUEST, "is_active": True}
        )()
        self.user_storage.get_user_data.return_value = self._mock_active_user()

        with pytest.raises(ModificationNotAllowed) as exc:
            self.interactor.add_member_to_workspace(dto)

        snapshot.assert_match(
            repr(exc.value),
            "add_workspace_member_no_edit_access.txt"
        )
