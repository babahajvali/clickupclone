from typing import Optional

from task_management.decorators.caching_decorators import \
    invalidate_interactor_cache
from task_management.interactors.dtos import WorkspaceDTO
from task_management.interactors.storage_interfaces import \
    WorkspaceStorageInterface
from task_management.interactors.workspaces.validators.workspace_validator import \
    WorkspaceValidator
from task_management.mixins import WorkspaceValidationMixin


class UpdateWorkspaceInteractor:

    def __init__(self, workspace_storage: WorkspaceStorageInterface):
        self.workspace_storage = workspace_storage

    @property
    def workspace_mixin(self) -> WorkspaceValidationMixin:
        return WorkspaceValidationMixin(
            workspace_storage=self.workspace_storage)
    
    @property
    def workspace_validator(self) -> WorkspaceValidator:
        return WorkspaceValidator(workspace_storage=self.workspace_storage)

    @invalidate_interactor_cache(cache_name="workspace_users")
    def update_workspace(
            self, workspace_id: str, user_id: str, name: Optional[str],
            description: Optional[str]) -> WorkspaceDTO:
        self.workspace_validator.check_workspace_update_field_properties(
            workspace_id=workspace_id, name=name, description=description
        )
        self.workspace_mixin.check_workspace_not_deleted(
            workspace_id=workspace_id
        )
        self.workspace_mixin.check_user_is_workspace_owner(
            user_id=user_id, workspace_id=workspace_id
        )

        return self.workspace_storage.update_workspace(
            workspace_id=workspace_id, name=name, description=description)
