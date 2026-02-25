import pytest
from unittest.mock import create_autospec

from task_management.exceptions.enums import Permissions, Visibility, Role
from task_management.interactors.dtos import WorkspaceMemberDTO
from task_management.interactors.spaces.space_interactor import SpaceInteractor
from task_management.interactors.storage_interfaces.space_storage_interface import SpaceStorageInterface
from task_management.interactors.storage_interfaces.workspace_storage_interface import WorkspaceStorageInterface
from task_management.exceptions.custom_exceptions import (
    ModificationNotAllowed,
    WorkspaceNotFound,
    DeletedWorkspaceFound,
    SpaceNotFound, DeletedSpaceFound,
)
from task_management.tests.factories.interactor_factory import (
    CreateSpaceDTOFactory,
    SpaceDTOFactory,
)


def make_workspace(is_deleted=False):
    return type('Workspace', (), {'is_deleted': is_deleted})()


def make_space(is_deleted=False, workspace_id="workspace_id_1"):
    return type('Space', (), {'is_deleted': is_deleted, 'workspace_id': workspace_id, 'order': 1})()


def make_permission(role: Role):
    return WorkspaceMemberDTO(
        id=1,
        workspace_id="workspace_id_1",
        role=role,
        user_id="user_id",
        is_active=True,
        added_by="admin"
    )


class TestSpaceInteractor:

    def setup_method(self):
        self.space_storage = create_autospec(SpaceStorageInterface)
        self.workspace_storage = create_autospec(WorkspaceStorageInterface)
        self.interactor = SpaceInteractor(
            space_storage=self.space_storage,
            workspace_storage=self.workspace_storage,
        )

    # ─── create_space ────────────────────────────────────────────

    def test_create_space_success(self):
        create_data = CreateSpaceDTOFactory()
        expected_result = SpaceDTOFactory()

        self.workspace_storage.get_workspace.return_value = make_workspace(is_deleted=False)
        self.workspace_storage.get_workspace_member.return_value = make_permission(role=Role.ADMIN)
        self.space_storage.get_last_space_order_in_workspace.return_value = 1
        self.space_storage.create_space.return_value = expected_result

        result = self.interactor.create_space(create_data)

        assert result == expected_result
        self.space_storage.create_space.assert_called_once()

    def test_create_space_workspace_not_found(self, snapshot):
        create_data = CreateSpaceDTOFactory()
        self.workspace_storage.get_workspace.return_value = None

        with pytest.raises(WorkspaceNotFound) as exc:
            self.interactor.create_space(create_data)

        snapshot.assert_match(repr(exc.value), "workspace_not_found.txt")

    def test_create_space_workspace_inactive(self, snapshot):
        create_data = CreateSpaceDTOFactory()
        self.workspace_storage.get_workspace.return_value = make_workspace(is_deleted=True)

        with pytest.raises(DeletedWorkspaceFound) as exc:
            self.interactor.create_space(create_data)

        snapshot.assert_match(repr(exc.value), "workspace_inactive.txt")

    def test_create_space_permission_denied(self, snapshot):
        create_data = CreateSpaceDTOFactory()
        self.workspace_storage.get_workspace.return_value = make_workspace(is_deleted=False)
        self.workspace_storage.get_workspace_member.return_value = make_permission(role=Role.GUEST)

        with pytest.raises(ModificationNotAllowed) as exc:
            self.interactor.create_space(create_data)

        snapshot.assert_match(repr(exc.value), "modification_not_allowed.txt")

    # ─── update_space ────────────────────────────────────────────

    def test_update_space_success(self):
        space_id = "space_id_1"
        user_id = "user_id"
        expected_result = SpaceDTOFactory()

        self.space_storage.get_space.return_value = make_space(is_deleted=False)
        self.space_storage.get_space_workspace_id.return_value = "workspace_id_1"
        self.workspace_storage.get_workspace_member.return_value = make_permission(role=Role.ADMIN)
        self.space_storage.update_space.return_value = expected_result

        result = self.interactor.update_space(
            space_id=space_id, user_id=user_id, name="New Name", description="New Desc")

        assert result == expected_result
        self.space_storage.update_space.assert_called_once()

    def test_update_space_not_found(self, snapshot):
        self.space_storage.get_space.return_value = None

        with pytest.raises(SpaceNotFound) as exc:
            self.interactor.update_space(
                space_id="bad_id", user_id="user_id", name="x", description=None)

        snapshot.assert_match(repr(exc.value), "space_not_found.txt")

    def test_update_space_inactive(self, snapshot):
        self.space_storage.get_space.return_value = make_space(is_deleted=True)

        with pytest.raises(DeletedSpaceFound) as exc:
            self.interactor.update_space(
                space_id="space_id_1", user_id="user_id", name="x", description=None)

        snapshot.assert_match(repr(exc.value), "space_inactive.txt")

    # ─── delete_space ────────────────────────────────────────────

    def test_delete_space_success(self):
        space_id = "space_id_1"
        user_id = "user_id"
        expected_result = SpaceDTOFactory()

        self.space_storage.get_space.return_value = make_space(is_deleted=False)
        self.space_storage.get_space_workspace_id.return_value = "workspace_id_1"
        self.workspace_storage.get_workspace_member.return_value = make_permission(role=Role.ADMIN)
        self.space_storage.delete_space.return_value = expected_result

        result = self.interactor.delete_space(space_id=space_id, deleted_by=user_id)

        assert result == expected_result
        self.space_storage.delete_space.assert_called_once_with(space_id=space_id)

    def test_delete_space_not_found(self, snapshot):
        self.space_storage.get_space_if_exists.return_value = False

        with pytest.raises(SpaceNotFound) as exc:
            self.interactor.delete_space(space_id="bad_id", deleted_by="user_id")

        snapshot.assert_match(repr(exc.value), "space_not_found.txt")

    # ─── set_space_visibility ─────────────────────────────────────

    def test_set_space_private_success(self):
        expected_result = SpaceDTOFactory()

        self.space_storage.get_space.return_value = make_space(is_deleted=False)
        self.space_storage.get_space_workspace_id.return_value = "workspace_id_1"
        self.workspace_storage.get_workspace_member.return_value = make_permission(role=Role.ADMIN)
        self.space_storage.update_space_visibility.return_value = expected_result

        result = self.interactor.set_space_visibility(
            space_id="space_id_1", user_id="user_id", visibility=Visibility.PRIVATE)

        assert result == expected_result
        self.space_storage.update_space_visibility.assert_called_once_with(
            space_id="space_id_1", visibility=Visibility.PRIVATE.value)

    def test_set_space_public_success(self):
        expected_result = SpaceDTOFactory()

        self.space_storage.get_space.return_value = make_space(is_deleted=False)
        self.space_storage.get_space_workspace_id.return_value = "workspace_id_1"
        self.workspace_storage.get_workspace_member.return_value = make_permission(role=Role.ADMIN)
        self.space_storage.update_space_visibility.return_value = expected_result

        result = self.interactor.set_space_visibility(
            space_id="space_id_1", user_id="user_id", visibility=Visibility.PUBLIC)

        assert result == expected_result
        self.space_storage.update_space_visibility.assert_called_once_with(
            space_id="space_id_1", visibility=Visibility.PUBLIC.value)

    # ─── get_workspace_spaces ─────────────────────────────────────

    def test_get_workspace_spaces_success(self):
        expected_result = [SpaceDTOFactory() for _ in range(3)]

        self.workspace_storage.get_workspace.return_value = make_workspace(is_deleted=False)
        self.space_storage.get_workspace_spaces.return_value = expected_result

        result = self.interactor.get_workspace_spaces(workspace_id="workspace_id_1")

        assert result == expected_result
        self.space_storage.get_workspace_spaces.assert_called_once_with(
            workspace_id="workspace_id_1")

    def test_get_workspace_spaces_workspace_not_found(self, snapshot):
        self.workspace_storage.get_workspace.return_value = None

        with pytest.raises(WorkspaceNotFound) as exc:
            self.interactor.get_workspace_spaces(workspace_id="bad_id")

        snapshot.assert_match(repr(exc.value), "workspace_not_found.txt")

    def test_get_workspace_spaces_workspace_inactive(self, snapshot):
        self.workspace_storage.get_workspace.return_value = make_workspace(is_deleted=True)

        with pytest.raises(DeletedWorkspaceFound) as exc:
            self.interactor.get_workspace_spaces(workspace_id="inactive_id")

        snapshot.assert_match(repr(exc.value), "workspace_inactive.txt")