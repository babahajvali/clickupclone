from task_management.decorators.caching_decorators import \
    invalidate_interactor_cache
from task_management.interactors.dtos import FieldDTO
from task_management.interactors.storage_interfaces import \
    FieldStorageInterface, WorkspaceStorageInterface
from task_management.mixins import WorkspaceValidationMixin, \
    FieldValidationMixin


class DeleteFieldInteractor(FieldValidationMixin, WorkspaceValidationMixin):
    """
    Delete field interactor soft delete the custom field in template

    This interactor can be used to delete the custom field
     check the permission before delete the custom field

    Key Responsibility:
     - Delete the custom field

    Dependencies:
        - FieldStorageInterface
        - WorkspaceStorageInterface
    """

    def __init__(
            self, field_storage: FieldStorageInterface,
            workspace_storage: WorkspaceStorageInterface):
        super().__init__(field_storage=field_storage,
                         workspace_storage=workspace_storage)
        self.field_storage = field_storage
        self.workspace_storage = workspace_storage

    @invalidate_interactor_cache(cache_name="fields")
    def delete_field(self, field_id: str, user_id: str) -> FieldDTO:
        """Soft delete a field after existence and permission checks."""
        self.check_field_exists(field_id=field_id)
        self._check_user_has_edit_access_to_field(
            field_id=field_id, user_id=user_id)

        return self.field_storage.delete_field(field_id=field_id)

    def _check_user_has_edit_access_to_field(
            self, field_id: str, user_id: str):
        workspace_id = self.field_storage.get_workspace_id_from_field_id(
            field_id=field_id)

        self.check_user_has_edit_access_to_workspace(
            workspace_id=workspace_id, user_id=user_id)
