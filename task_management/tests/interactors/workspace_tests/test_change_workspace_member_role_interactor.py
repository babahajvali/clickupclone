from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import (
    UnexpectedRole,
    ModificationNotAllowed,
    InactiveUser,
    DeletedWorkspaceFound,
    UserNotWorkspaceMember, InactiveWorkspaceMember,
)
from task_management.exceptions.enums import Role
from task_management.interactors.storage_interfaces.user_storage_interface import (
    UserStorageInterface
)
from task_management.interactors.storage_interfaces.workspace_storage_interface import (
    WorkspaceStorageInterface
)
from task_management.interactors.workspaces.change_workspace_member_role_interactor import (
    ChangeWorkspaceMemberRoleInteractor
)
from task_management.tests.factories.interactor_factory import (
    WorkspaceMemberDTOFactory,
)


class TestChangeWorkspaceMemberRoleInteractor:

    def setup_method(self):
        self.workspace_storage = create_autospec(WorkspaceStorageInterface)
        self.user_storage = create_autospec(UserStorageInterface)

        self.interactor = ChangeWorkspaceMemberRoleInteractor(
            workspace_storage=self.workspace_storage,
            user_storage=self.user_storage,
        )

    @staticmethod
    def _mock_active_workspace():
        return type("Workspace", (), {
            "workspace_id": "workspace123",
            "user_id": "admin123",
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

    def test_change_member_role_success(self):
        expected = WorkspaceMemberDTOFactory(role=Role.ADMIN)

        self.workspace_storage.get_workspace.return_value = (
            self._mock_active_workspace()
        )
        self.user_storage.get_user_data.return_value = self._mock_active_user()

        # target member active
        self.workspace_storage.get_workspace_member.side_effect = [
            type("WorkspaceMember", (),
                 {"role": Role.ADMIN, "is_active": True})(),
            # for check_workspace_member_is_active
            type("WorkspaceMember", (), {"role": Role.ADMIN})(),
            # for permission check (changed_by)
        ]

        self.workspace_storage.update_the_member_role.return_value = expected

        result = self.interactor.change_member_role(
            workspace_id="workspace123",
            user_id="user123",
            role=Role.ADMIN.value,
            changed_by="admin123"
        )

        assert result == expected

    def test_change_member_workspace_deleted(self, snapshot):
        self.workspace_storage.get_workspace.return_value = (
            self._mock_deleted_workspace()
        )

        with pytest.raises(DeletedWorkspaceFound) as exc:
            self.interactor.change_member_role(
                workspace_id="workspace123",
                user_id="user123",
                role=Role.ADMIN.value,
                changed_by="admin123"
            )

        snapshot.assert_match(
            repr(exc.value),
            "change_workspace_role_workspace_deleted.txt"
        )

    def test_change_member_user_inactive(self, snapshot):
        self.workspace_storage.get_workspace.return_value = (
            self._mock_active_workspace()
        )
        self.user_storage.get_user_data.return_value = (
            self._mock_inactive_user()
        )

        with pytest.raises(InactiveUser) as exc:
            self.interactor.change_member_role(
                workspace_id="workspace123",
                user_id="user123",
                role=Role.ADMIN.value,
                changed_by="admin123"
            )

        snapshot.assert_match(
            repr(exc.value),
            "change_workspace_role_user_inactive.txt"
        )

    def test_change_member_target_not_active(self, snapshot):
        self.workspace_storage.get_workspace.return_value = (
            self._mock_active_workspace()
        )
        self.user_storage.get_user_data.return_value = self._mock_active_user()

        # target member inactive
        self.workspace_storage.get_workspace_member.return_value = type(
            "WorkspaceMember", (),
            {'id': 1, "role": Role.ADMIN, "is_active": False}
        )()

        with pytest.raises(InactiveWorkspaceMember) as exc:
            self.interactor.change_member_role(
                workspace_id="workspace123",
                user_id="user123",
                role=Role.ADMIN.value,
                changed_by="admin123"
            )

        snapshot.assert_match(
            repr(exc.value),
            "change_workspace_role_target_inactive.txt"
        )

    def test_change_member_changed_by_not_member(self, snapshot):
        self.workspace_storage.get_workspace.return_value = (
            self._mock_active_workspace()
        )
        self.user_storage.get_user_data.return_value = self._mock_active_user()

        # target member active
        self.workspace_storage.get_workspace_member.side_effect = [
            type("WorkspaceMember", (),
                 {"role": Role.ADMIN, "is_active": True})(),
            None,  # changed_by not found
        ]

        with pytest.raises(UserNotWorkspaceMember) as exc:
            self.interactor.change_member_role(
                workspace_id="workspace123",
                user_id="user123",
                role=Role.ADMIN.value,
                changed_by="admin123"
            )

        snapshot.assert_match(
            repr(exc.value),
            "change_workspace_role_changed_by_not_member.txt"
        )

    def test_change_member_changed_by_insufficient_role(self, snapshot):
        self.workspace_storage.get_workspace.return_value = (
            self._mock_active_workspace()
        )
        self.user_storage.get_user_data.return_value = self._mock_active_user()

        self.workspace_storage.get_workspace_member.side_effect = [
            type("WorkspaceMember", (),
                 {"role": Role.ADMIN, "is_active": True})(),
            type("WorkspaceMember", (), {"role": Role.MEMBER})(),
        ]

        with pytest.raises(ModificationNotAllowed) as exc:
            self.interactor.change_member_role(
                workspace_id="workspace123",
                user_id="user123",
                role=Role.ADMIN.value,
                changed_by="member123"
            )

        snapshot.assert_match(
            repr(exc.value),
            "change_workspace_role_insufficient_permission.txt"
        )

    def test_change_member_invalid_role(self, snapshot):
        self.workspace_storage.get_workspace.return_value = (
            self._mock_active_workspace()
        )
        self.user_storage.get_user_data.return_value = self._mock_active_user()

        self.workspace_storage.get_workspace_member.side_effect = [
            type("WorkspaceMember", (),
                 {"role": Role.ADMIN, "is_active": True})(),
            type("WorkspaceMember", (), {"role": Role.ADMIN})(),
        ]

        with pytest.raises(UnexpectedRole) as exc:
            self.interactor.change_member_role(
                workspace_id="workspace123",
                user_id="user123",
                role="INVALID",
                changed_by="admin123"
            )

        snapshot.assert_match(
            repr(exc.value),
            "change_workspace_role_invalid_role.txt"
        )
