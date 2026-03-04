from django.db import transaction

from task_management.exceptions.enums import PermissionType
from task_management.interactors.dtos import CreateSpaceDTO, SpaceDTO, \
    CreateUserSpacePermissionDTO, UserSpacePermissionDTO
from task_management.interactors.spaces.add_space_permission_for_user_interactor import \
    AddSpacePermissionForUser
from task_management.interactors.spaces.create_space_interactor import \
    CreateSpaceInteractor
from task_management.interactors.storage_interfaces import \
    SpaceStorageInterface, WorkspaceStorageInterface


class SpaceCreationHandler:

    def __init__(
            self, space_storage: SpaceStorageInterface,
            workspace_storage: WorkspaceStorageInterface):
        self.space_storage = space_storage
        self.workspace_storage = workspace_storage

    @transaction.atomic
    def handle_space_creation(self, space_input: CreateSpaceDTO) -> SpaceDTO:
        space_data = self._create_space(space_input=space_input)

        if space_data.is_private:
            self._create_space_permission_for_user(
                space_id=space_data.space_id, user_id=space_data.created_by
            )

        return space_data

    def _create_space(self, space_input: CreateSpaceDTO) -> SpaceDTO:
        space_interactor = CreateSpaceInteractor(
            space_storage=self.space_storage,
            workspace_storage=self.workspace_storage)

        return space_interactor.create_space(space_data=space_input)

    def _create_space_permission_for_user(
            self, space_id: str, user_id: str) -> UserSpacePermissionDTO:
        permission_interactor = AddSpacePermissionForUser(
            space_storage=self.space_storage,
            workspace_storage=self.workspace_storage
        )

        user_permission_data = CreateUserSpacePermissionDTO(
            space_id=space_id,
            user_id=user_id,
            permission_type=PermissionType.FULL_EDIT,
            added_by=user_id
        )

        return permission_interactor.add_user_for_space_permission(
            user_data=user_permission_data)
