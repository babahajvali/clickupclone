from django.db import transaction

from task_management.exceptions.custom_exceptions import \
    NothingToUpdateField
from task_management.interactors.dtos import CreateFieldDTO, FieldDTO, \
    UpdateFieldDTO

from task_management.decorators.caching_decorators import interactor_cache, \
    invalidate_interactor_cache
from task_management.interactors.storage_interfaces import \
    FieldStorageInterface, TemplateStorageInterface, WorkspaceStorageInterface
from task_management.interactors.fields.validators.field_validator import \
    FieldValidator
from task_management.interactors.fields.validators.field_config_validator \
    import FieldConfigValidator
from task_management.mixins import TemplateValidationMixin, \
    WorkspaceValidationMixin, FieldValidationMixin


class FieldInteractor:
    """Field Management Business Logic Interactor.
    
    Handles all fields-related operations including creation, updating,
     deletion, reordering, and retrieval of fields within templates.
    This interactor enforces business rules and validates user permissions
     before performing any fields operations.

    Key Responsibilities:
        - Create new fields with validation
        - Update existing fields properties
        - Delete fields with permission checks
        - Reorder fields within templates
        - Retrieve fields for specific templates
        - Validate fields configurations and types
    
    Dependencies:
        - FieldStorageInterface: Field data persistence
        - TemplateStorageInterface: Template validation and access
        - WorkspaceStorageInterface: User permission validation

    Attributes:
        field_storage (FieldStorageInterface): Storage for fields operations
        template_storage (TemplateStorageInterface): Storage for template
         operations
        workspace_storage (WorkspaceStorageInterface): validate the user
         permissions
    """

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
    def create_field(self, field_data: CreateFieldDTO) -> FieldDTO:

        self.template_mixin.check_template_exists(
            template_id=field_data.template_id)
        self.check_user_has_edit_access_to_template(
            template_id=field_data.template_id,
            user_id=field_data.created_by_user_id
        )
        self._create_field_input_validation(field_data=field_data)
        self.field_validator.check_field_name_not_exist_in_template(
            field_name=field_data.field_name,
            template_id=field_data.template_id,
            field_id=None
        )

        last_field_order_in_template = (
            self.field_storage.get_next_field_order_in_template(
                template_id=field_data.template_id))

        return self.field_storage.create_field(
            create_field_data=field_data, order=last_field_order_in_template)

    @invalidate_interactor_cache(cache_name="fields")
    def update_field(
            self, update_field_data: UpdateFieldDTO, user_id: str) -> FieldDTO:

        self.field_mixin.check_field_is_active(
            field_id=update_field_data.field_id)
        field_data = self.field_storage.get_field_by_id(
            field_id=update_field_data.field_id)
        self._check_update_field_properties(
            update_field_data=update_field_data, field_data=field_data
        )
        self.check_user_has_edit_access_to_template(
            template_id=field_data.template_id, user_id=user_id
        )

        return self.field_storage.update_field(
            field_id=update_field_data.field_id,
            update_field_data=update_field_data)

    @transaction.atomic
    @invalidate_interactor_cache(cache_name="fields")
    def reorder_field(self, field_id: str, template_id: str, new_order: int,
                      user_id: str) -> FieldDTO:

        self.template_mixin.check_template_exists(template_id=template_id)
        self.field_mixin.check_field_is_active(field_id=field_id)
        self.check_user_has_edit_access_to_template(
            template_id=template_id, user_id=user_id)
        self.field_validator.check_field_order(
            template_id=template_id, order=new_order)

        field_dto = self.field_storage.get_field_by_id(field_id=field_id)
        old_order = field_dto.order

        if old_order == new_order:
            return field_dto

        self.field_validator.reorder_field_positions(
            template_id=template_id, new_order=new_order, old_order=old_order
        )

        return self.field_storage.update_field_order(
            field_id=field_id, new_order=new_order)

    @invalidate_interactor_cache(cache_name="fields")
    def delete_field(self, field_id: str, user_id: str) -> FieldDTO:

        self.field_mixin.check_field_is_active(field_id=field_id)
        field_data = self.field_storage.get_field_by_id(
            field_id=field_id)
        self.check_user_has_edit_access_to_template(
            template_id=field_data.template_id, user_id=user_id)

        return self.field_storage.delete_field(field_id=field_id)

    @interactor_cache(cache_name="fields", timeout=5 * 60)
    def get_active_fields_for_template(
            self, template_id: str) -> list[FieldDTO]:

        self.template_mixin.check_template_exists(template_id=template_id)

        return self.field_storage.get_fields_for_template(
            template_id=template_id)

    def get_field(self, field_id: str) -> FieldDTO:

        self.field_mixin.check_field_is_active(field_id=field_id)

        return self.field_storage.get_field_by_id(field_id=field_id)

    def check_user_has_edit_access_to_template(
            self, template_id: str, user_id: str):

        workspace_id = self.template_storage.get_workspace_id_from_template_id(
            template_id=template_id)

        self.workspace_mixin.check_user_has_access_to_workspace(
            workspace_id=workspace_id, user_id=user_id)

    # Helping functions

    def _create_field_input_validation(self, field_data: CreateFieldDTO):

        self.field_validator.check_field_name_not_empty(
            field_name=field_data.field_name)
        self.field_validator.check_field_type(
            field_type=field_data.field_type.value)
        self.field_config_validator.check_config(
            config=field_data.config, field_type=field_data.field_type)

    def _check_update_field_properties(
            self, update_field_data: UpdateFieldDTO, field_data: FieldDTO):

        if not self.field_validator.is_field_properties_not_empty(
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
