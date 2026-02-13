from django.db import transaction

from task_management.exceptions.enums import Permissions
from task_management.interactors.dtos import CreateSpaceDTO, SpaceDTO, \
    CreateUserSpacePermissionDTO
from task_management.interactors.space.space_interactor import SpaceInteractor
from task_management.interactors.storage_interfaces import \
    SpaceStorageInterface, WorkspaceStorageInterface


class SpaceOnboardingHandler:

    def __init__(self, space_storage: SpaceStorageInterface,
                 workspace_storage: WorkspaceStorageInterface):
        self.space_storage = space_storage
        self.workspace_storage = workspace_storage

    @transaction.atomic
    def handle_space(self, space_input: CreateSpaceDTO) -> SpaceDTO:

        space_data = self._create_space(space_input=space_input)

        if space_data.is_private:
            self._create_space_permission_for_user(
                space_id=space_data.space_id, user_id=space_data.created_by)

        return space_data

    def _get_space_interactor(self):

        space_interactor = SpaceInteractor(
            space_storage=self.space_storage,
            workspace_storage=self.workspace_storage)

        return space_interactor

    def _create_space(self, space_input: CreateSpaceDTO) -> SpaceDTO:

        space_interactor = self._get_space_interactor()

        return space_interactor.create_space(space_data=space_input)

    def _create_space_permission_for_user(self, space_id: str, user_id: str):
        space_interactor = self._get_space_interactor()

        user_permission_data = CreateUserSpacePermissionDTO(
            space_id=space_id,
            user_id=user_id,
            permission_type=Permissions.FULL_EDIT,
            added_by=user_id
        )

        return space_interactor.add_user_for_space_permission(
            user_data=user_permission_data)
