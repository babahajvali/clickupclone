from task_management.decorators.caching_decorators import \
    invalidate_interactor_cache
from task_management.exceptions.custom_exceptions import \
    NothingToUpdateWorkspace
from task_management.interactors.dtos import WorkspaceDTO, UpdateWorkspaceDTO
from task_management.interactors.storage_interfaces import \
    WorkspaceStorageInterface
from task_management.mixins import WorkspaceValidationMixin


class UpdateWorkspaceInteractor(WorkspaceValidationMixin):

    def __init__(self, workspace_storage: WorkspaceStorageInterface):
        super().__init__(workspace_storage=workspace_storage)
        self.workspace_storage = workspace_storage

    @invalidate_interactor_cache(cache_name="workspace_users")
    def update_workspace(
            self, update_workspace_dto: UpdateWorkspaceDTO,
            user_id: str) -> WorkspaceDTO:
        self._check_workspace_update_field_properties(
            update_workspace_dto=update_workspace_dto
        )

        self.check_workspace_not_deleted(
            workspace_id=update_workspace_dto.workspace_id
        )
        self.check_user_is_workspace_owner(
            user_id=user_id,
            workspace_id=update_workspace_dto.workspace_id,
        )

        return self.workspace_storage.update_workspace(
            workspace_id=update_workspace_dto.workspace_id,
            name=update_workspace_dto.name,
            description=update_workspace_dto.description,
        )

    def _check_workspace_update_field_properties(
            self, update_workspace_dto: UpdateWorkspaceDTO):

        has_name_provided = update_workspace_dto.name is not None
        has_description_provided = update_workspace_dto.description is not None
        has_no_update_field_properties = not (
                has_description_provided or has_name_provided
        )
        if has_no_update_field_properties:
            raise NothingToUpdateWorkspace(
                workspace_id=update_workspace_dto.workspace_id
            )
        if has_name_provided:
            self.check_workspace_name_not_empty(
                workspace_name=update_workspace_dto.name
            )
