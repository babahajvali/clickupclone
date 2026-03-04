from task_management.decorators.caching_decorators import \
    invalidate_interactor_cache
from task_management.exceptions.custom_exceptions import NothingToUpdateField
from task_management.interactors.dtos import UpdateFieldDTO, FieldDTO
from task_management.interactors.fields.validators.field_config_validator import \
    FieldConfigValidator
from task_management.interactors.fields.validators.field_validator import \
    FieldValidator
from task_management.interactors.storage_interfaces import \
    FieldStorageInterface, WorkspaceStorageInterface
from task_management.mixins import WorkspaceValidationMixin, \
    FieldValidationMixin


class UpdateFieldInteractor:
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
        - TemplateStorageInterface
    """

    def __init__(
            self, field_storage: FieldStorageInterface,
            workspace_storage: WorkspaceStorageInterface):
        self.field_storage = field_storage
        self.workspace_storage = workspace_storage

    @property
    def workspace_mixin(self) -> WorkspaceValidationMixin:
        return WorkspaceValidationMixin(
            workspace_storage=self.workspace_storage)

    @property
    def field_mixin(self) -> FieldValidationMixin:
        return FieldValidationMixin(field_storage=self.field_storage)

    @property
    def field_config_validator(self) -> FieldConfigValidator:
        return FieldConfigValidator()

    @property
    def field_validator(self) -> FieldValidator:
        return FieldValidator(field_storage=self.field_storage)

    @invalidate_interactor_cache(cache_name="fields")
    def update_field(
            self, update_field_data: UpdateFieldDTO, user_id: str) -> FieldDTO:
        """Update field metadata/config for a template field."""

        self.field_mixin.check_field_not_deleted(
            field_id=update_field_data.field_id)

        field_data = self.field_storage.get_field(
            field_id=update_field_data.field_id)
        self._check_update_field_properties(
            update_field_data=update_field_data, field_data=field_data
        )
        self._check_user_has_edit_access_to_field(
            field_id=field_data.field_id, user_id=user_id
        )

        return self.field_storage.update_field(
            field_id=update_field_data.field_id,
            update_field_data=update_field_data)

    def _check_update_field_properties(
            self, update_field_data: UpdateFieldDTO, field_data: FieldDTO):
        self._validate_update_field_not_empty(update_field_data, field_data)
        self._validate_update_field_name(update_field_data, field_data)
        self._validate_update_field_config(update_field_data, field_data)

    def _validate_update_field_not_empty(
            self, update_field_data: UpdateFieldDTO, field_data: FieldDTO):
        if not self._is_field_properties_not_empty(
                update_field_data=update_field_data):
            raise NothingToUpdateField(field_id=field_data.field_id)

    def _validate_update_field_name(
            self, update_field_data: UpdateFieldDTO, field_data: FieldDTO):
        is_field_name_provided = update_field_data.field_name is not None
        if not is_field_name_provided:
            return
        self.field_validator.check_field_name_not_empty(
            field_name=update_field_data.field_name)
        self.field_validator.check_field_name_not_exist_in_template(
            field_id=update_field_data.field_id,
            field_name=update_field_data.field_name,
            template_id=field_data.template_id)

    def _validate_update_field_config(
            self, update_field_data: UpdateFieldDTO, field_data: FieldDTO):
        is_config_provided = update_field_data.config is not None
        if not is_config_provided:
            return
        self.field_config_validator.check_field_config(
            field_type=field_data.field_type,
            config=update_field_data.config)

    @staticmethod
    def _is_field_properties_not_empty(
            update_field_data: UpdateFieldDTO) -> bool:

        return any([
            update_field_data.field_name is not None,
            update_field_data.config is not None,
            update_field_data.description is not None,
            update_field_data.is_required is not None])

    def _check_user_has_edit_access_to_field(
            self, field_id: str, user_id: str):
        workspace_id = self.field_storage.get_workspace_id_from_field_id(
            field_id=field_id)

        self.workspace_mixin.check_user_has_edit_access_to_workspace(
            workspace_id=workspace_id, user_id=user_id)
