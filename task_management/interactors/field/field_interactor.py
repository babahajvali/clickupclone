from django.core.exceptions import ObjectDoesNotExist

from task_management.exceptions.custom_exceptions import \
    NothingToUpdateFieldException, UnsupportedFieldTypeException, \
    FieldNameAlreadyExistsException
from task_management.exceptions.enums import FieldType
from task_management.interactors.dtos import CreateFieldDTO, FieldDTO, \
    UpdateFieldDTO

from task_management.decorators.caching_decorators import interactor_cache, \
    invalidate_interactor_cache
from task_management.interactors.storage_interfaces import \
    FieldStorageInterface, TemplateStorageInterface, WorkspaceStorageInterface
from task_management.mixins import TemplateValidationMixin, \
    FieldValidationMixin, WorkspaceValidationMixin


class FieldInteractor(TemplateValidationMixin, WorkspaceValidationMixin,
                      FieldValidationMixin):
    """Field Management Business Logic Interactor.
    
    Handles all field-related operations including creation, updating, deletion,
    reordering, and retrieval of field within templates. This interactor
    enforces business rules and validates user permissions before performing
    any field operations.
    
    Key Responsibilities:
        - Create new field with validation
        - Update existing field properties
        - Delete field with permission checks
        - Reorder field within templates
        - Retrieve field for specific templates
        - Validate field configurations and types
    
    Dependencies:
        - FieldStorageInterface: Field data persistence
        - TemplateStorageInterface: Template validation and access
        - WorkspaceStorageInterface: User permission validation

    Attributes:
        field_storage (FieldStorageInterface): Storage for field operations
        template_storage (TemplateStorageInterface): Storage for template operations
        workspace_storage (WorkspaceStorageInterface): validate the user permissions
    """

    def __init__(self, field_storage: FieldStorageInterface,
                 template_storage: TemplateStorageInterface,
                 workspace_storage: WorkspaceStorageInterface):
        super().__init__(template_storage=template_storage,
                         workspace_storage=workspace_storage,
                         field_storage=field_storage)
        self.field_storage = field_storage
        self.template_storage = template_storage
        self.workspace_storage = workspace_storage

    @invalidate_interactor_cache(cache_name="field")
    def create_field(self, field_data: CreateFieldDTO) -> FieldDTO:

        self.create_field_input_validation(field_data=field_data)
        self.check_template_exists(template_id=field_data.template_id)
        self.check_field_name_not_exist_in_template(
            field_name=field_data.field_name,
            template_id=field_data.template_id)
        self.check_user_has_edit_access_to_template(
            template_id=field_data.template_id,
            user_id=field_data.created_by_user_id)

        last_field_order_in_template = (
            self.field_storage.get_active_last_field_order_in_template(
                template_id=field_data.template_id))

        return self.field_storage.create_field(
            create_field_data=field_data, order=last_field_order_in_template)

    @invalidate_interactor_cache(cache_name="field")
    def update_field(self, update_field_data: UpdateFieldDTO,
                     user_id: str) -> FieldDTO:

        self.check_field_is_active(field_id=update_field_data.field_id)
        field_data = self.field_storage.get_active_field_by_id(
            field_id=update_field_data.field_id)
        self.update_field_properties_validation(
            update_field_data=update_field_data, field_data=field_data)
        self.check_user_has_edit_access_to_template(
            template_id=field_data.template_id, user_id=user_id)

        return self.field_storage.update_field(
            field_id=update_field_data.field_id,
            update_field_data=update_field_data)

    @invalidate_interactor_cache(cache_name="field")
    def reorder_field(self, field_id: str, template_id: str, new_order: int,
                      user_id: str) -> FieldDTO:

        self.check_template_exists(template_id=template_id)
        self.check_field_is_active(field_id=field_id)
        self.check_field_order(template_id=template_id, order=new_order)

        self.check_user_has_edit_access_to_template(template_id=template_id,
                                                    user_id=user_id)

        return self.field_storage.reorder_fields(
            field_id=field_id, template_id=template_id, new_order=new_order)

    @invalidate_interactor_cache(cache_name="field")
    def delete_field(self, field_id: str, user_id: str) -> FieldDTO:

        self.check_field_is_active(field_id=field_id)
        field_data = self.field_storage.get_active_field_by_id(
            field_id=field_id)
        self.check_user_has_edit_access_to_template(
            template_id=field_data.template_id, user_id=user_id)

        return self.field_storage.delete_field(field_id=field_id)

    @interactor_cache(cache_name="field", timeout=5 * 60)
    def get_active_fields_for_template(self, template_id: str) -> list[
        FieldDTO]:

        self.check_template_exists(template_id=template_id)

        return self.field_storage.get_active_fields_for_template(
            template_id=template_id)

    def get_active_field(self, field_id: str) -> FieldDTO:

        self.check_field_is_active(field_id=field_id)

        return self.field_storage.get_active_field_by_id(field_id=field_id)

    def check_user_has_edit_access_to_template(self, template_id: str,
                                               user_id: str):
        """Validate user has access to workspace containing the template."""
        workspace_id = self.template_storage.get_workspace_id_from_template_id(
            template_id=template_id)

        self.validate_user_has_access_to_workspace(
            workspace_id=workspace_id, user_id=user_id)

    # Helping functions

    def create_field_input_validation(self, field_data: CreateFieldDTO):

        self.check_field_name_not_empty(field_name=field_data.field_name)
        self.check_field_type(field_type=field_data.field_type.value)
        self.check_config(config=field_data.config,
                          field_type=field_data.field_type)

    def update_field_properties_validation(
            self, update_field_data: UpdateFieldDTO, field_data: FieldDTO):

        if not self._has_any_update(update_field_data=update_field_data):
            raise NothingToUpdateFieldException(field_id=field_data.field_id)

        is_field_name_provided = update_field_data.field_name is not None
        if is_field_name_provided:
            self.check_field_name_not_empty(
                field_name=update_field_data.field_name)
            self.check_field_name_in_db_except_current_field(
                field_id=update_field_data.field_id,
                field_name=update_field_data.field_name,
                template_id=field_data.template_id)

        is_config_provided = update_field_data.config is not None
        if is_config_provided:
            self.check_field_config(field_type=field_data.field_type,
                                    config=update_field_data.config)

    @staticmethod
    def _has_any_update(update_field_data: UpdateFieldDTO) -> bool:
        return any([
            update_field_data.field_name is not None,
            update_field_data.config is not None,
            update_field_data.description is not None,
            update_field_data.is_required is not None])

    @staticmethod
    def check_field_type(field_type: str):
        field_types = FieldType.get_values()
        is_field_type_invalid = field_type not in field_types

        if is_field_type_invalid:
            raise UnsupportedFieldTypeException(field_type=field_type)

    def check_field_name_not_exist_in_template(self, field_name: str,
                                               template_id: str):

        try:
            field_data = self.field_storage.get_field_by_name(
                field_name=field_name, template_id=template_id)
        except ObjectDoesNotExist:
            pass
        else:
            is_field_exists = field_data is not None
            if is_field_exists:
                raise FieldNameAlreadyExistsException(field_name=field_name)