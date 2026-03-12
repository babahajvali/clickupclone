from typing import Optional, Dict

from task_management.decorators.caching_decorators import \
    invalidate_interactor_cache
from task_management.exceptions.custom_exceptions import NothingToUpdateField
from task_management.exceptions.enums import FieldType
from task_management.interactors.dtos import UpdateFieldDTO, FieldDTO
from task_management.interactors.fields.validators.field_config_validator import \
    FieldConfigValidator
from task_management.interactors.storage_interfaces import \
    FieldStorageInterface, WorkspaceStorageInterface
from task_management.mixins import WorkspaceValidationMixin, \
    FieldValidationMixin
from task_management.utils.redis_utils import redis_lock


class UpdateFieldInteractor(FieldValidationMixin, WorkspaceValidationMixin):
    """
    Update Field Interactor update the custom field in template

    Handle the update field operation
    This interactor check the business rules and input validation
     and permission validation before update the custom field

    Key Responsibility:
     - Update the custom field

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

    @property
    def field_config_validator(self) -> FieldConfigValidator:
        return FieldConfigValidator()

    @invalidate_interactor_cache(cache_name="fields")
    def update_field(
            self, update_field_dto: UpdateFieldDTO, user_id: str) -> FieldDTO:
        """Update field metadata/config for a template field."""

        self.check_field_not_deleted(
            field_id=update_field_dto.field_id)

        field_dto = self.check_field_exists(
            field_id=update_field_dto.field_id)

        self._check_update_field_properties_not_empty(
            update_field_dto=update_field_dto)
        self._check_user_has_edit_access_to_field(
            field_id=field_dto.field_id, user_id=user_id
        )

        lock_key = f"lock:update_field:{update_field_dto.field_id}"

        with redis_lock(lock_key, timeout=10):
            self._check_update_field_name(
                field_name=update_field_dto.field_name,
                field_id=update_field_dto.field_id,
                template_id=field_dto.template_id)
            self._check_update_field_config(
                field_type=field_dto.field_type,
                config=update_field_dto.config)

            field_dto = self.field_storage.update_field(
                update_field_dto=update_field_dto)
        return field_dto

    @staticmethod
    def _check_update_field_properties_not_empty(
            update_field_dto: UpdateFieldDTO):

        is_field_properties_empty = not any([
            update_field_dto.field_name is not None,
            update_field_dto.config is not None,
            update_field_dto.description is not None,
            update_field_dto.is_required is not None])

        if is_field_properties_empty:
            raise NothingToUpdateField(field_id=update_field_dto.field_id)

    def _check_update_field_name(
            self, field_name: Optional[str], field_id: str, template_id: str):
        is_field_name_provided = field_name is not None
        if not is_field_name_provided:
            return
        self.check_field_name_not_empty(
            field_name=field_name)
        self.check_field_name_not_exist_in_template(
            field_id=field_id,
            field_name=field_name,
            template_id=template_id)

    def _check_update_field_config(
            self, field_type: FieldType, config: Optional[Dict]):
        is_config_provided = config is not None
        if not is_config_provided:
            return
        self.field_config_validator.check_field_config(
            field_type=field_type,
            config=config)

    def _check_user_has_edit_access_to_field(
            self, field_id: str, user_id: str):
        workspace_id = self.field_storage.get_workspace_id_from_field_id(
            field_id=field_id)

        self.check_user_has_edit_access_to_workspace(
            workspace_id=workspace_id, user_id=user_id)
