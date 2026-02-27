from task_management.decorators.caching_decorators import \
    invalidate_interactor_cache
from task_management.exceptions.custom_exceptions import UnsupportedFieldType
from task_management.exceptions.enums import FieldType
from task_management.interactors.dtos import CreateFieldDTO, FieldDTO
from task_management.interactors.fields.validators.field_config_validator import \
    FieldConfigValidator
from task_management.interactors.fields.validators.field_validator import \
    FieldValidator
from task_management.interactors.storage_interfaces import \
    FieldStorageInterface, TemplateStorageInterface, WorkspaceStorageInterface
from task_management.mixins import TemplateValidationMixin, \
    WorkspaceValidationMixin


class CreateFieldInteractor:

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
    def field_config_validator(self) -> FieldConfigValidator:
        return FieldConfigValidator()

    @property
    def field_validator(self) -> FieldValidator:
        return FieldValidator(field_storage=self.field_storage)

    @invalidate_interactor_cache(cache_name="fields")
    def create_field(self, field_data: CreateFieldDTO) -> FieldDTO:
        self._create_field_input_validation(field_data=field_data)
        self.template_mixin.check_template_exists(
            template_id=field_data.template_id)
        self._check_user_has_edit_access_to_template(
            template_id=field_data.template_id,
            user_id=field_data.created_by_user_id
        )

        last_field_order_in_template = (
            self.field_storage.get_last_field_order_in_template(
                template_id=field_data.template_id))

        return self.field_storage.create_field(
            create_field_data=field_data,
            order=last_field_order_in_template + 1)

    def _create_field_input_validation(self, field_data: CreateFieldDTO):
        self.field_validator.check_field_name_not_empty(
            field_name=field_data.field_name)
        self._check_field_type(field_type=field_data.field_type.value)
        self.field_config_validator.check_config(
            config=field_data.config, field_type=field_data.field_type)
        self.field_validator.check_field_name_not_exist_in_template(
            field_name=field_data.field_name,
            template_id=field_data.template_id,
            field_id=None
        )

    def _check_user_has_edit_access_to_template(
            self, template_id: str, user_id: str):
        workspace_id = self.template_storage.get_workspace_id_from_template_id(
            template_id=template_id)

        self.workspace_mixin.check_user_has_edit_access_to_workspace(
            workspace_id=workspace_id, user_id=user_id)

    @staticmethod
    def _check_field_type(field_type: str):
        existed_field_types = FieldType.get_values()
        is_invalid_field_type = field_type not in existed_field_types

        if is_invalid_field_type:
            raise UnsupportedFieldType(field_type=field_type)
