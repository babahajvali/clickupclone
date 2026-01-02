import pytest
from unittest.mock import create_autospec


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

from task_management.exceptions.custom_exceptions import (
    NotAccessToModificationException,
    UnexpectedRoleFoundException
)
from task_management.exceptions.enums import PermissionsEnum, RoleEnum
from task_management.interactors.workspace_interactors.workspace_member_interactors import \
    WorkspaceMemberInteractor
from task_management.tests.factories.interactor_factory import (
    AddMemberToWorkspaceDTOFactory,
    WorkspaceMemberDTOFactory
)





class TestWorkspaceMemberInteractor:

    def setup_method(self):
        self.workspace_storage = create_autospec(WorkspaceStorageInterface)
        self.workspace_member_storage = create_autospec(WorkspaceMemberStorageInterface)
        self.user_storage = create_autospec(UserStorageInterface)
        self.permission_storage = create_autospec(SpacePermissionStorageInterface)

        self.interactor = WorkspaceMemberInteractor(
            workspace_member_storage=self.workspace_member_storage,
            workspace_storage=self.workspace_storage,
            user_storage=self.user_storage,
            permission_storage=self.permission_storage
        )


    def _mock_active_workspace(self, owner_id="admin123"):
        return type(
            "Workspace",
            (),
            {
                "workspace_id": "workspace123",
                "owner_id": owner_id,
                "is_active": True
            }
        )()

    def _mock_active_user(self):
        return type(
            "User",
            (),
            {
                "is_active": True
            }
        )()

    # ---------- add member ----------

    def test_add_member_to_workspace_success(self, snapshot):
        dto = AddMemberToWorkspaceDTOFactory()
        expected = WorkspaceMemberDTOFactory()

        self.workspace_storage.get_workspace.return_value = self._mock_active_workspace(
            owner_id=dto.added_by
        )
        self.user_storage.get_user_data.return_value = self._mock_active_user()
        self.workspace_member_storage.add_member_to_workspace.return_value = expected

        result = self.interactor.add_member_to_workspace(dto)

        assert result == expected
        # snapshot.assert_match(repr(result), "add_member_success.txt")

        self.workspace_member_storage.add_member_to_workspace.assert_called_once_with(
            workspace_member_data=dto
        )

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

        workspace = self._mock_active_workspace(owner_id="someone_else")
        self.workspace_storage.get_workspace.return_value = workspace
        self.user_storage.get_user_data.return_value = self._mock_active_user()

        self.workspace_member_storage.get_workspace_member.return_value = (type("WorkspaceMember",(),{"role": RoleEnum.GUEST.value})())


        with pytest.raises(NotAccessToModificationException) as exc:
            self.interactor.add_member_to_workspace(dto)

        snapshot.assert_match(repr(exc.value), "add_member_permission_denied.txt")

    # ---------- remove member ----------

    def test_remove_member_success(self, snapshot):
        expected = WorkspaceMemberDTOFactory()

        self.workspace_storage.get_workspace.return_value = self._mock_active_workspace(
            owner_id="admin123"
        )
        self.user_storage.get_user_data.return_value = self._mock_active_user()
        self.workspace_member_storage.remove_member_from_workspace.return_value = expected

        result = self.interactor.remove_member_from_workspace(
            user_id="user123",
            workspace_id="workspace123",
            removed_by="admin123"
        )
        assert result == expected

        # snapshot.assert_match(repr(result), "remove_member_success.txt")

    # ---------- change role ----------

    def test_change_member_role_success(self, snapshot):
        expected = WorkspaceMemberDTOFactory(role=RoleEnum.MEMBER)

        self.workspace_storage.get_workspace.return_value = self._mock_active_workspace(
            owner_id="admin123"
        )
        self.user_storage.get_user_data.return_value = self._mock_active_user()
        self.workspace_member_storage.update_the_member_role.return_value = expected

        result = self.interactor.change_member_role(
            workspace_id="workspace123",
            user_id="user123",
            role=RoleEnum.MEMBER,
            changed_by="admin123"
        )
        assert result == expected

        # snapshot.assert_match(repr(result.workspace_id), "change_role_success.txt")

    def test_change_member_role_invalid_role(self, snapshot):
        self.workspace_storage.get_workspace.return_value = self._mock_active_workspace()
        self.user_storage.get_user_data.return_value = self._mock_active_user()

        with pytest.raises(UnexpectedRoleFoundException) as exc:
            self.interactor.change_member_role(
                workspace_id="workspace123",
                user_id="user123",
                role=type("Role", (), {"value": "INVALID"})(),
                changed_by="admin123"
            )

        snapshot.assert_match(repr(exc.value), "change_role_invalid.txt")
