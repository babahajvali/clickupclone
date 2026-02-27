from task_management.decorators.caching_decorators import \
    invalidate_interactor_cache
from task_management.exceptions.custom_exceptions import NothingToUpdateField
from task_management.interactors.dtos import UpdateFieldDTO, FieldDTO
from task_management.interactors.fields.validators.field_config_validator import \
    FieldConfigValidator
from task_management.interactors.fields.validators.field_validator import \
    FieldValidator
from task_management.interactors.storage_interfaces import \
    FieldStorageInterface, TemplateStorageInterface, WorkspaceStorageInterface
from task_management.mixins import TemplateValidationMixin, \
    WorkspaceValidationMixin, FieldValidationMixin


class UpdateFieldInteractor:

    def __init__(self, field_storage: FieldStorageInterface,
                 template_storage: TemplateStorageInterface,
                 workspace_storage: WorkspaceStorageInterface):
        self.field_storage = field_storage
        self.template_storage = template_storage
        self.workspace_storage = workspace_storage

    @property
    def template_mixin(self) -> TemplateValidationMixin:
        return TemplateValidationMixin(template_storage=self.template_storage)

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

        self.field_mixin.check_field_is_active(
            field_id=update_field_data.field_id)

        field_data = self.field_storage.get_field(
            field_id=update_field_data.field_id)
        self._check_update_field_properties(
            update_field_data=update_field_data, field_data=field_data
        )
        self._check_user_has_edit_access_to_template(
            template_id=field_data.template_id, user_id=user_id
        )

        return self.field_storage.update_field(
            field_id=update_field_data.field_id,
            update_field_data=update_field_data)

    def _check_update_field_properties(
            self, update_field_data: UpdateFieldDTO, field_data: FieldDTO):

        if not self._is_field_properties_not_empty(
                update_field_data=update_field_data):
            raise NothingToUpdateField(field_id=field_data.field_id)

        is_field_name_provided = update_field_data.field_name is not None
        if is_field_name_provided:
            self.field_validator.check_field_name_not_empty(
                field_name=update_field_data.field_name)
            self.field_validator.check_field_name_not_exist_in_template(
                field_id=update_field_data.field_id,
                field_name=update_field_data.field_name,
                template_id=field_data.template_id)

        is_config_provided = update_field_data.config is not None
        if is_config_provided:
            self.field_config_validator.check_config(
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

    def _check_user_has_edit_access_to_template(
            self, template_id: str, user_id: str):
        workspace_id = self.template_storage.get_workspace_id_from_template_id(
            template_id=template_id)

        self.workspace_mixin.check_user_has_edit_access_to_workspace(
            workspace_id=workspace_id, user_id=user_id)
