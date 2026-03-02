from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import (
    ModificationNotAllowed, InactiveWorkspaceMember,
)
from task_management.exceptions.enums import Role
from task_management.interactors.storage_interfaces.workspace_storage_interface import (
    WorkspaceStorageInterface
)
from task_management.interactors.workspaces.remove_workspace_member_interactor import (
    RemoveWorkspaceMemberInteractor
)
from task_management.tests.factories.interactor_factory import (
    WorkspaceMemberDTOFactory,
)


class TestRemoveWorkspaceMemberInteractor:

    def setup_method(self):
        self.workspace_storage = create_autospec(WorkspaceStorageInterface)

        self.interactor = RemoveWorkspaceMemberInteractor(
            workspace_storage=self.workspace_storage,
        )

    @staticmethod
    def _mock_active_workspace_member(workspace_id="workspace123"):
        return type("WorkspaceMember", (), {
            "id": 1,
            "workspace_id": workspace_id,
            "role": Role.ADMIN,
            "is_active": True
        })()

    @staticmethod
    def _mock_inactive_workspace_member(workspace_id="workspace123"):
        return type("WorkspaceMember", (), {
            "id": 1,
            "workspace_id": workspace_id,
            "role": Role.ADMIN,
            "is_active": False
        })()

    def test_remove_member_success(self):
        expected = WorkspaceMemberDTOFactory()

        active_member = self._mock_active_workspace_member()

        self.workspace_storage.get_workspace_member_by_id.return_value = active_member
        self.workspace_storage.get_workspace_member.return_value = type(
            "WorkspaceMember", (), {"role": Role.ADMIN, "is_active": True}
        )()

        self.workspace_storage.remove_member_from_workspace.return_value = expected

        result = self.interactor.remove_member_from_workspace(
            workspace_member_id=1,
            removed_by="admin123"
        )

        assert result == expected
        self.workspace_storage.remove_member_from_workspace.assert_called_once_with(
            workspace_member_id=1
        )

    def test_remove_member_not_active(self, snapshot):
        self.workspace_storage.get_workspace_member_by_id.return_value = (
            self._mock_inactive_workspace_member()
        )

        with pytest.raises(InactiveWorkspaceMember) as exc:
            self.interactor.remove_member_from_workspace(
                workspace_member_id=1,
                removed_by="admin123"
            )

        snapshot.assert_match(
            repr(exc.value),
            "remove_workspace_member_not_active.txt"
        )

    def test_remove_member_no_edit_access(self, snapshot):
        active_member = self._mock_active_workspace_member()

        self.workspace_storage.get_workspace_member_by_id.return_value = active_member

        self.workspace_storage.get_workspace_member.return_value = type(
            "WorkspaceMember", (), {"role": Role.GUEST, "is_active": True}
        )()

        with pytest.raises(ModificationNotAllowed) as exc:
            self.interactor.remove_member_from_workspace(
                workspace_member_id=1,
                removed_by="guest123"
            )

        snapshot.assert_match(
            repr(exc.value),
            "remove_workspace_member_no_edit_access.txt"
        )
