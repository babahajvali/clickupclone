from task_management.decorators.caching_decorators import \
    invalidate_interactor_cache
from task_management.exceptions.custom_exceptions import UnsupportedFieldType
from task_management.exceptions.enums import FieldType
from task_management.interactors.dtos import CreateFieldDTO, FieldDTO
from task_management.interactors.fields.validators.field_config_validator import \
    FieldConfigValidator
from task_management.interactors.storage_interfaces import \
    FieldStorageInterface, TemplateStorageInterface, WorkspaceStorageInterface
from task_management.mixins import TemplateValidationMixin, \
    WorkspaceValidationMixin, FieldValidationMixin


class CreateFieldInteractor(TemplateValidationMixin, WorkspaceValidationMixin,
                            FieldValidationMixin):
    """
    Create Field Interactor create the custom field for template

    Handle the create field Operation
    This interactor check the business rules and input validation
     and permission validation before create the custom field

    Key Responsibility:
     - Create the custom field

    Dependencies:
        - FieldStorageInterface
        - WorkspaceStorageInterface
        - TemplateStorageInterface
    """

    def __init__(
            self, field_storage: FieldStorageInterface,
            template_storage: TemplateStorageInterface,
            workspace_storage: WorkspaceStorageInterface):
        super().__init__(
            template_storage=template_storage,
            workspace_storage=workspace_storage,
            field_storage=field_storage
        )
        self.field_storage = field_storage
        self.template_storage = template_storage
        self.workspace_storage = workspace_storage

    @property
    def field_config_validator(self) -> FieldConfigValidator:
        return FieldConfigValidator()

    @invalidate_interactor_cache(cache_name="fields")
    def create_field(self, create_field_dto: CreateFieldDTO) -> FieldDTO:
        """Create a new custom field for the target template."""
        self._check_create_field_input(create_field_dto=create_field_dto)
        self._check_user_has_edit_access_to_template(
            template_id=create_field_dto.template_id,
            user_id=create_field_dto.created_by_user_id,
        )

        last_field_order_in_template = (
            self.field_storage.get_last_field_order_in_template(
                template_id=create_field_dto.template_id
            )
        )

        return self.field_storage.create_field(
            create_field_dto=create_field_dto,
            order=last_field_order_in_template + 1,
        )

    def _check_create_field_input(self, create_field_dto: CreateFieldDTO):
        self.check_field_name_not_empty(
            field_name=create_field_dto.field_name
        )
        self._check_invalid_field_type(
            field_type=create_field_dto.field_type.value
        )
        self.field_config_validator.check_field_config(
            config=create_field_dto.config,
            field_type=create_field_dto.field_type,
        )
        self.check_field_name_not_exist_in_template(
            field_name=create_field_dto.field_name,
            template_id=create_field_dto.template_id,
            field_id=None
        )

        self.check_template_exists(
            template_id=create_field_dto.template_id
        )

    def _check_user_has_edit_access_to_template(
            self, template_id: str, user_id: str):
        workspace_id = self.template_storage.get_workspace_id_from_template_id(
            template_id=template_id)

        self.check_user_has_edit_access_to_workspace(
            workspace_id=workspace_id, user_id=user_id)

    @staticmethod
    def _check_invalid_field_type(field_type: str):
        existed_field_types = FieldType.get_values()
        is_invalid_field_type = field_type not in existed_field_types

        if is_invalid_field_type:
            raise UnsupportedFieldType(field_type=field_type)
