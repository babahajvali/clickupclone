from task_management.decorators.caching_decorators import \
    invalidate_interactor_cache
from task_management.exceptions.custom_exceptions import \
    WorkspaceMemberIdNotFound, InactiveWorkspaceMember
from task_management.interactors.dtos import WorkspaceMemberDTO
from task_management.interactors.storage_interfaces import \
    WorkspaceStorageInterface
from task_management.mixins import WorkspaceValidationMixin


class RemoveWorkspaceMemberInteractor:

    def __init__(self, workspace_storage: WorkspaceStorageInterface):
        self.workspace_storage = workspace_storage

    @property
    def workspace_mixin(self) -> WorkspaceValidationMixin:
        return WorkspaceValidationMixin(
            workspace_storage=self.workspace_storage)

    @invalidate_interactor_cache(cache_name="user_workspaces")
    @invalidate_interactor_cache(cache_name='validate_permission')
    def remove_member_from_workspace(
            self, workspace_member_id: int, removed_by: str) \
            -> WorkspaceMemberDTO:
        self._check_workspace_member_is_active_by_id(
            workspace_member_id=workspace_member_id
        )
        workspace_member_data = self.workspace_storage.get_workspace_member_by_id(
            workspace_member_id=workspace_member_id
        )
        self.workspace_mixin.check_user_has_edit_access_to_workspace(
            user_id=removed_by,
            workspace_id=workspace_member_data.workspace_id
        )

        return self.workspace_storage.remove_member_from_workspace(
            workspace_member_id=workspace_member_id
        )

    def _check_workspace_member_is_active_by_id(
            self, workspace_member_id: int):
        workspace_member_data = self.workspace_storage.get_workspace_member_by_id(
            workspace_member_id=workspace_member_id)

        is_member_not_found = not workspace_member_data

        if is_member_not_found:
            raise WorkspaceMemberIdNotFound(
                workspace_member_id=workspace_member_id)

        if not workspace_member_data.is_active:
            raise InactiveWorkspaceMember(
                workspace_member_id=workspace_member_id)
