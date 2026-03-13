from task_management.exceptions.custom_exceptions import InvalidPermission
from task_management.exceptions.enums import PermissionType
from task_management.interactors.dtos import UserSpacePermissionDTO, \
    CreateUserSpacePermissionDTO
from task_management.interactors.storage_interfaces import \
    SpaceStorageInterface, WorkspaceStorageInterface
from task_management.mixins import SpaceValidationMixin, \
    WorkspaceValidationMixin


class AddSpacePermissionForUserInteractor(
    SpaceValidationMixin, WorkspaceValidationMixin):
    """
    Add Space Permission For User Interactor grants space-level access.

    Handle the add space permission operation.
    This interactor checks the business rules and permission validation
     before granting access.

    Key Responsibility:
     - Add user permission for a space

    Dependencies:
        - SpaceStorageInterface
        - WorkspaceStorageInterface
    """

    def __init__(
            self, space_storage: SpaceStorageInterface,
            workspace_storage: WorkspaceStorageInterface):
        super().__init__(
            space_storage=space_storage,
            workspace_storage=workspace_storage
        )
        self.space_storage = space_storage
        self.workspace_storage = workspace_storage

    def add_user_for_space_permission(
            self, create_space_permission_dto: CreateUserSpacePermissionDTO) \
            -> UserSpacePermissionDTO:
        """Grant a space permission entry for a user."""
        self.check_space_not_deleted(
            space_id=create_space_permission_dto.space_id)
        self.check_user_has_edit_access_space_permission(
            space_id=create_space_permission_dto.space_id,
            user_id=create_space_permission_dto.added_by)
        self._check_permission_type_is_valid(
            permission=create_space_permission_dto.permission_type.value)

        return self.space_storage.create_user_space_permissions(
            permission_dtos=[create_space_permission_dto])[0]

    @staticmethod
    def _check_permission_type_is_valid(permission: str):
        existed_permissions = PermissionType.get_values()
        is_invalid_permission_type = permission not in existed_permissions

        if is_invalid_permission_type:
            raise InvalidPermission(permission=permission)
