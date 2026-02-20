import pytest
from unittest.mock import create_autospec

from task_management.exceptions.custom_exceptions import (
    ModificationNotAllowed,
    UnexpectedRole
)
from task_management.exceptions.enums import  Role
from task_management.interactors.workspace.workspace_member_interactor import (
    WorkspaceMemberInteractor
)

from task_management.interactors.storage_interfaces.workspace_storage_interface import (
    WorkspaceStorageInterface
)
from task_management.interactors.storage_interfaces.user_storage_interface import (
    UserStorageInterface
)

from task_management.tests.factories.interactor_factory import (
    AddMemberToWorkspaceDTOFactory,
    WorkspaceMemberDTOFactory
)


class TestWorkspaceMemberInteractor:

    def setup_method(self):
        self.workspace_storage = create_autospec(WorkspaceStorageInterface)
        self.user_storage = create_autospec(UserStorageInterface)

        self.interactor = WorkspaceMemberInteractor(
            workspace_storage=self.workspace_storage,
            user_storage=self.user_storage,
        )

    @staticmethod
    def _mock_active_workspace(owner_id="admin123"):
        return type("Workspace",(),
            {
                "workspace_id": "workspace123",
                "user_id": owner_id,
                "is_active": True
            })()

    @staticmethod
    def _mock_active_user():
        return type("User", (), {"is_active": True})()

    @staticmethod
    def _mock_space(space_id="space123"):
        return type("Space", (), {"space_id": space_id})()

    @staticmethod
    def _mock_folder(folder_id="folder123"):
        return type("Folder", (), {"folder_id": folder_id})()

    @staticmethod
    def _mock_list(list_id="list123"):
        return type("List", (), {"list_id": list_id})()


    def test_add_member_to_workspace_success(self):
        dto = AddMemberToWorkspaceDTOFactory()
        expected = WorkspaceMemberDTOFactory()

        self.workspace_storage.get_workspaces.return_value = (
            self._mock_active_workspace(owner_id=dto.added_by)
        )
        self.workspace_storage.get_workspace_member.return_value = type("WorkspaceMember", (), {'role': Role.MEMBER, 'is_active': True})()
        self.user_storage.get_user_data.return_value = self._mock_active_user()
        self.workspace_storage.add_member_to_workspace.return_value = expected

        result = self.interactor.add_member_to_workspace(dto)

        assert result.role == expected.role

    def test_add_member_invalid_role(self, snapshot):
        dto = AddMemberToWorkspaceDTOFactory()
        dto.role = type("Role", (), {"value": "INVALID"})()

        self.workspace_storage.get_workspaces.return_value = self._mock_active_workspace()
        self.user_storage.get_user_data.return_value = self._mock_active_user()
        self.workspace_storage.get_workspace_member.return_value = None

        with pytest.raises(UnexpectedRole) as exc:
            self.interactor.add_member_to_workspace(dto)

        snapshot.assert_match(repr(exc.value), "add_member_invalid_role.txt")

    def test_add_member_permission_denied(self, snapshot):
        dto = AddMemberToWorkspaceDTOFactory()

        self.workspace_storage.get_workspaces.return_value = (
            self._mock_active_workspace(owner_id="someone_else")
        )
        self.user_storage.get_user_data.return_value = self._mock_active_user()

        self.workspace_storage.get_workspace_member.return_value = None

        with pytest.raises(ModificationNotAllowed) as exc:
            self.interactor.add_member_to_workspace(dto)

        snapshot.assert_match(
            repr(exc.value),
            "add_member_permission_denied.txt"
        )


    def test_remove_member_success(self):
        expected = WorkspaceMemberDTOFactory()

        self.workspace_storage.get_workspaces.return_value = self._mock_active_workspace()
        self.user_storage.get_user_data.return_value = self._mock_active_user()
        self.workspace_storage.remove_member_from_workspace.return_value = expected

        result = self.interactor.remove_member_from_workspace(
            removed_by="user123",
            workspace_member_id=1)
        assert result == expected

        # snapshot.assert_match(repr(result), "remove_member_success.txt")


    def test_change_member_role_success(self):
        expected = WorkspaceMemberDTOFactory(role=Role.MEMBER)

        self.workspace_storage.get_workspaces.return_value = self._mock_active_workspace()
        self.user_storage.get_user_data.return_value = self._mock_active_user()
        self.workspace_storage.update_the_member_role.return_value = expected


        result = self.interactor.change_member_role(
            workspace_id="workspace123",
            user_id="user123",
            role=Role.MEMBER.value,
            changed_by="admin123"
        )
        assert result == expected

        # snapshot.assert_match(repr(result), "change_role_success.txt")

    def test_change_member_role_invalid(self, snapshot):
        self.workspace_storage.get_workspaces.return_value = self._mock_active_workspace()
        self.user_storage.get_user_data.return_value = self._mock_active_user()

        with pytest.raises(UnexpectedRole) as exc:
            self.interactor.change_member_role(
                workspace_id="workspace123",
                user_id="user123",
                role=type("Role", (), {"value": "INVALID"})(),
                changed_by="admin123"
            )

        snapshot.assert_match(repr(exc.value),"change_role_invalid.txt")
