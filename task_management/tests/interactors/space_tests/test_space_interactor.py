import pytest
from unittest.mock import create_autospec

from task_management.exceptions.enums import PermissionsEnum, Visibility, Role
from task_management.interactors.dtos import UserSpacePermissionDTO
from task_management.interactors.space_interactors.space_interactors import \
    SpaceInteractor
from task_management.interactors.storage_interface.space_storage_interface import \
    SpaceStorageInterface
from task_management.interactors.storage_interface.folder_storage_interface import \
    FolderStorageInterface
from task_management.interactors.storage_interface.list_storage_interface import \
    ListStorageInterface
from task_management.interactors.storage_interface.space_permission_storage_interface import \
    SpacePermissionStorageInterface
from task_management.interactors.storage_interface.workspace_storage_interface import \
    WorkspaceStorageInterface
from task_management.interactors.storage_interface.workspace_member_storage_interface import \
    WorkspaceMemberStorageInterface
from task_management.exceptions.custom_exceptions import (
    ModificationNotAllowedException,
    WorkspaceNotFoundException,
    InactiveWorkspaceException,
    SpaceNotFoundException,
)
from task_management.tests.factories.interactor_factory import (
    CreateSpaceDTOFactory,
    SpaceDTOFactory
)


def make_permission(permission_type: PermissionsEnum):
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
        self.folder_storage = create_autospec(FolderStorageInterface)
        self.list_storage = create_autospec(ListStorageInterface)
        self.permission_storage = create_autospec(
            SpacePermissionStorageInterface)
        self.workspace_storage = create_autospec(WorkspaceStorageInterface)
        self.workspace_member_storage = create_autospec(
            WorkspaceMemberStorageInterface)

        self.interactor = SpaceInteractor(
            space_storage=self.space_storage,
            folder_storage=self.folder_storage,
            list_storage=self.list_storage,
            permission_storage=self.permission_storage,
            workspace_storage=self.workspace_storage,
            workspace_member_storage=self.workspace_member_storage
        )

    def test_create_space_success(self):
        # Arrange
        create_data = CreateSpaceDTOFactory()
        expected_result = SpaceDTOFactory()

        self.permission_storage.get_user_permission_for_space.return_value = make_permission(
            PermissionsEnum.FULL_EDIT.value)
        self.workspace_storage.get_workspace.return_value = type(
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

        self.workspace_storage.get_workspace.return_value = type(
            "Workspace", (), {
                "is_active": True,
                "user_id": "some-other-user"
            }
        )()

        self.workspace_member_storage.get_workspace_member.return_value = type(
            "Member", (), {
                "role": Role.GUEST
            }
        )()


        with pytest.raises(ModificationNotAllowedException) as exc:
            self.interactor.create_space(create_data)

        snapshot.assert_match(
            repr(exc.value),
            "test_create_space_permission_denied.txt"
        )

    def test_create_space_workspace_not_found(self, snapshot):
        # Arrange
        create_data = CreateSpaceDTOFactory()
        self.permission_storage.get_user_permission_for_space.return_value = make_permission(
            PermissionsEnum.FULL_EDIT.value)
        self.workspace_storage.get_workspace.return_value = None

        # Act & Assert
        with pytest.raises(WorkspaceNotFoundException) as exc:
            self.interactor.create_space(create_data)

        snapshot.assert_match(repr(exc.value), "workspace_not_found.txt")

    def test_create_space_workspace_inactive(self, snapshot):
        # Arrange
        create_data = CreateSpaceDTOFactory()
        self.permission_storage.get_user_permission_for_space.return_value = make_permission(
            PermissionsEnum.FULL_EDIT.value)
        self.workspace_storage.get_workspace.return_value = type('Workspace',
                                                                 (), {
                                                                     'is_active': False})()

        # Act & Assert
        with pytest.raises(InactiveWorkspaceException) as exc:
            self.interactor.create_space(create_data)

        snapshot.assert_match(repr(exc.value), "workspace_inactive.txt")

    def test_update_space_success(self):
        # Arrange
        update_data = SpaceDTOFactory()
        expected_result = SpaceDTOFactory()

        self.permission_storage.get_user_permission_for_space.return_value = make_permission(
            PermissionsEnum.FULL_EDIT.value)
        self.space_storage.get_space.return_value = type('Space', (),
                                                         {'is_active': True,
                                                          "workspace_id": "workspace_id_1"})()
        self.workspace_storage.get_workspace.return_value = type('Workspace',
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
        self.permission_storage.get_user_permission_for_space.return_value = make_permission(
            PermissionsEnum.FULL_EDIT.value)
        self.space_storage.get_space.return_value = None

        # Act & Assert
        with pytest.raises(SpaceNotFoundException) as exc:
            self.interactor.update_space(update_data, user_id="user_id")

        snapshot.assert_match(repr(exc.value), "space_not_found.txt")

    def test_delete_space_success(self):
        # Arrange
        space_id = "test-space-id"
        user_id = "test-user-id"
        expected_result = SpaceDTOFactory()

        self.permission_storage.get_user_permission_for_space.return_value = make_permission(
            PermissionsEnum.FULL_EDIT.value)
        self.space_storage.get_space.return_value = type('Space', (),
                                                         {'is_active': True})()
        self.space_storage.remove_space.return_value = expected_result

        # Act
        result = self.interactor.delete_space(space_id, user_id)

        # Assert
        assert result == expected_result
        self.space_storage.remove_space.assert_called_once_with(
            space_id=space_id)

    def test_set_space_private_success(self):
        # Arrange
        space_id = "test-space-id"
        user_id = "test-user-id"
        expected_result = SpaceDTOFactory()

        self.permission_storage.get_user_permission_for_space.return_value = make_permission(
            PermissionsEnum.FULL_EDIT.value)
        self.space_storage.get_space.return_value = type('Space', (),
                                                         {'is_active': True})()
        self.space_storage.set_space_private.return_value = expected_result

        # Act
        result = self.interactor.set_space_visibility(space_id, user_id,Visibility.PRIVATE)

        # Assert
        assert result == expected_result
        self.space_storage.set_space_private.assert_called_once_with(
            space_id=space_id)

    def test_set_space_public_success(self):
        # Arrange
        space_id = "test-space-id"
        user_id = "test-user-id"
        expected_result = SpaceDTOFactory()

        self.permission_storage.get_user_permission_for_space.return_value = make_permission(
            PermissionsEnum.FULL_EDIT.value)
        self.space_storage.get_space.return_value = type('Space', (),
                                                         {'is_active': True})()
        self.space_storage.set_space_public.return_value = expected_result

        # Act
        result = self.interactor.set_space_visibility(space_id, user_id,Visibility.PUBLIC)

        # Assert
        assert result == expected_result
        self.space_storage.set_space_public.assert_called_once_with(
            space_id=space_id)

    def test_get_workspace_spaces_success(self):
        # Arrange
        workspace_id = "test-workspace-id"
        expected_result = [SpaceDTOFactory() for _ in range(3)]

        self.workspace_storage.get_workspace.return_value = type('Workspace',
                                                                 (), {
                                                                     'is_active': True})()
        self.space_storage.get_workspace_spaces.return_value = expected_result

        # Act
        result = self.interactor.get_workspace_spaces(workspace_id)

        # Assert
        assert result == expected_result
        self.space_storage.get_workspace_spaces.assert_called_once_with(
            workspace_id=workspace_id)

    def test_get_workspace_spaces_workspace_not_found(self, snapshot):
        # Arrange
        workspace_id = "non-existent-workspace"
        self.workspace_storage.get_workspace.return_value = None

        # Act & Assert
        with pytest.raises(WorkspaceNotFoundException) as exc:
            self.interactor.get_workspace_spaces(workspace_id)

        snapshot.assert_match(repr(exc.value), "workspace_not_found.txt")

    def test_get_workspace_spaces_workspace_inactive(self, snapshot):
        # Arrange
        workspace_id = "inactive-workspace"
        self.workspace_storage.get_workspace.return_value = type('Workspace',
                                                                 (), {
                                                                     'is_active': False})()

        # Act & Assert
        with pytest.raises(InactiveWorkspaceException) as exc:
            self.interactor.get_workspace_spaces(workspace_id)

        snapshot.assert_match(repr(exc.value), "workspace_inactive.txt")
