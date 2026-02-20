import pytest
from unittest.mock import create_autospec

from task_management.exceptions.enums import Permissions, Visibility, Role
from task_management.interactors.dtos import UserSpacePermissionDTO
from task_management.interactors.spaces.space_interactor import \
    SpaceInteractor
from task_management.interactors.storage_interfaces.space_storage_interface import \
    SpaceStorageInterface
from task_management.interactors.storage_interfaces.workspace_storage_interface import \
    WorkspaceStorageInterface

from task_management.exceptions.custom_exceptions import (
    ModificationNotAllowed,
    WorkspaceNotFound,
    InactiveWorkspace,
    SpaceNotFound,
)
from task_management.tests.factories.interactor_factory import (
    CreateSpaceDTOFactory,
    SpaceDTOFactory
)


def make_permission(permission_type: Permissions):
    return UserSpacePermissionDTO(
        id=1,
        space_id="space_id",
        permission_type=permission_type,
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

    def test_create_space_success(self):
        # Arrange
        create_data = CreateSpaceDTOFactory()
        expected_result = SpaceDTOFactory()

        self.space_storage.get_user_permission_for_space.return_value = make_permission(
            Permissions.FULL_EDIT.value)
        self.workspace_storage.get_active_workspaces.return_value = type(
            'Workspace', (), {
                'is_active': True,
                'user_id': create_data.created_by
            }
        )()

        self.space_storage.create_space.return_value = expected_result

        # Act
        result = self.interactor.create_space(create_data)

        # Assert
        assert result == expected_result
        self.space_storage.create_space.assert_called_once_with(create_data)

    def test_create_space_permission_denied(self, snapshot):
        create_data = CreateSpaceDTOFactory()

        self.workspace_storage.get_active_workspaces.return_value = type(
            "Workspace", (), {
                "is_active": True,
                "user_id": "some-other-user"
            }
        )()

        self.workspace_storage.get_workspace_member.return_value = type(
            "Member", (), {
                "role": Role.GUEST
            }
        )()

        with pytest.raises(ModificationNotAllowed) as exc:
            self.interactor.create_space(create_data)

        snapshot.assert_match(
            repr(exc.value),
            "test_create_space_permission_denied.txt"
        )

    def test_create_space_workspace_not_found(self, snapshot):
        # Arrange
        create_data = CreateSpaceDTOFactory()
        self.space_storage.get_user_permission_for_space.return_value = make_permission(
            Permissions.FULL_EDIT.value)
        self.workspace_storage.get_active_workspaces.return_value = None

        # Act & Assert
        with pytest.raises(WorkspaceNotFound) as exc:
            self.interactor.create_space(create_data)

        snapshot.assert_match(repr(exc.value), "workspace_not_found.txt")

    def test_create_space_workspace_inactive(self, snapshot):
        # Arrange
        create_data = CreateSpaceDTOFactory()
        self.space_storage.get_user_permission_for_space.return_value = make_permission(
            Permissions.FULL_EDIT.value)
        self.workspace_storage.get_active_workspaces.return_value = type('Workspace',
                                                                         (), {
                                                                     'is_active': False})()

        # Act & Assert
        with pytest.raises(InactiveWorkspace) as exc:
            self.interactor.create_space(create_data)

        snapshot.assert_match(repr(exc.value), "workspace_inactive.txt")

    def test_update_space_success(self):
        # Arrange
        update_data = SpaceDTOFactory()
        expected_result = SpaceDTOFactory()

        self.space_storage.get_user_permission_for_space.return_value = make_permission(
            Permissions.FULL_EDIT.value)
        self.space_storage.get_space.return_value = type('Space', (),
                                                         {'is_active': True,
                                                          "workspace_id": "workspace_id_1"})()
        self.workspace_storage.get_active_workspaces.return_value = type('Workspace',
                                                                         (), {
                                                                     'is_active': True})()
        self.space_storage.update_space.return_value = expected_result

        # Act
        result = self.interactor.update_space(update_data, user_id="user_id")

        # Assert
        assert result == expected_result
        self.space_storage.update_space.assert_called_once_with(update_data)

    def test_update_space_not_found(self, snapshot):
        # Arrange
        update_data = SpaceDTOFactory()
        self.space_storage.get_user_permission_for_space.return_value = make_permission(
            Permissions.FULL_EDIT.value)
        self.space_storage.get_space.return_value = None

        # Act & Assert
        with pytest.raises(SpaceNotFound) as exc:
            self.interactor.update_space(update_data, user_id="user_id")

        snapshot.assert_match(repr(exc.value), "space_not_found.txt")

    def test_delete_space_success(self):
        # Arrange
        space_id = "test-spaces-id"
        user_id = "test-user-id"
        expected_result = SpaceDTOFactory()

        self.space_storage.get_user_permission_for_space.return_value = make_permission(
            Permissions.FULL_EDIT.value)
        self.space_storage.get_space.return_value = type('Space', (),
                                                         {'is_active': True})()
        self.space_storage.delete_space.return_value = expected_result

        # Act
        result = self.interactor.delete_space(space_id, user_id)

        # Assert
        assert result == expected_result
        self.space_storage.delete_space.assert_called_once_with(
            space_id=space_id)

    def test_set_space_private_success(self):
        # Arrange
        space_id = "test-spaces-id"
        user_id = "test-user-id"
        expected_result = SpaceDTOFactory()

        self.space_storage.get_user_permission_for_space.return_value = make_permission(
            Permissions.FULL_EDIT.value)
        self.space_storage.get_space.return_value = type('Space', (),
                                                         {'is_active': True})()
        self.space_storage.set_space_private.return_value = expected_result

        # Act
        result = self.interactor.set_space_visibility(space_id, user_id,
                                                      Visibility.PRIVATE)

        # Assert
        assert result == expected_result
        self.space_storage.set_space_private.assert_called_once_with(
            space_id=space_id)

    def test_set_space_public_success(self):
        # Arrange
        space_id = "test-spaces-id"
        user_id = "test-user-id"
        expected_result = SpaceDTOFactory()

        self.space_storage.get_user_permission_for_space.return_value = make_permission(
            Permissions.FULL_EDIT.value)
        self.space_storage.get_space.return_value = type('Space', (),
                                                         {'is_active': True})()
        self.space_storage.set_space_public.return_value = expected_result

        # Act
        result = self.interactor.set_space_visibility(space_id, user_id,
                                                      Visibility.PUBLIC)

        # Assert
        assert result == expected_result
        self.space_storage.set_space_public.assert_called_once_with(
            space_id=space_id)

    def test_get_workspace_spaces_success(self):
        # Arrange
        workspace_id = "test-workspaces-id"
        expected_result = [SpaceDTOFactory() for _ in range(3)]

        self.workspace_storage.get_active_workspaces.return_value = type('Workspace',
                                                                         (), {
                                                                     'is_active': True})()
        self.space_storage.get_active_workspace_spaces.return_value = expected_result

        # Act
        result = self.interactor.get_active_workspace_spaces(workspace_id)

        # Assert
        assert result == expected_result
        self.space_storage.get_active_workspace_spaces.assert_called_once_with(
            workspace_id=workspace_id)

    def test_get_workspace_spaces_workspace_not_found(self, snapshot):
        # Arrange
        workspace_id = "non-existent-workspaces"
        self.workspace_storage.get_active_workspaces.return_value = None

        # Act & Assert
        with pytest.raises(WorkspaceNotFound) as exc:
            self.interactor.get_active_workspace_spaces(workspace_id)

        snapshot.assert_match(repr(exc.value), "workspace_not_found.txt")

    def test_get_workspace_spaces_workspace_inactive(self, snapshot):
        # Arrange
        workspace_id = "inactive-workspaces"
        self.workspace_storage.get_active_workspaces.return_value = type('Workspace',
                                                                         (), {
                                                                     'is_active': False})()

        # Act & Assert
        with pytest.raises(InactiveWorkspace) as exc:
            self.interactor.get_active_workspace_spaces(workspace_id)

        snapshot.assert_match(repr(exc.value), "workspace_inactive.txt")
