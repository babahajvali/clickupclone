from django.db import transaction

from task_management.exceptions.enums import PermissionType
from task_management.interactors.dtos import CreateSpaceDTO, SpaceDTO, \
    CreateUserSpacePermissionDTO, UserSpacePermissionDTO
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
    def handle_space_creation(
            self, space_input_dto: CreateSpaceDTO) -> SpaceDTO:
        space_dto = self._create_space(create_space_dto=space_input_dto)

        if space_dto.is_private:
            self._create_space_permission_for_user(
                space_id=space_dto.space_id, user_id=space_dto.created_by
            )

        return space_dto

    def _create_space(self, create_space_dto: CreateSpaceDTO) -> SpaceDTO:
        space_interactor = CreateSpaceInteractor(
            space_storage=self.space_storage,
            workspace_storage=self.workspace_storage)

        return space_interactor.create_space(
            create_space_dto=create_space_dto
        )

    def _create_space_permission_for_user(
            self, space_id: str, user_id: str) -> UserSpacePermissionDTO:
        user_permission_dto = CreateUserSpacePermissionDTO(
            space_id=space_id,
            user_id=user_id,
            permission_type=PermissionType.FULL_EDIT,
            added_by=user_id
        )

        return self.space_storage.create_user_space_permissions(
            permission_dtos=[user_permission_dto])[0]
