from task_management.exceptions.custom_exceptions import \
    InvalidOrderException, MissingFieldConfigException, \
    NothingToUpdateFieldException, EmptyNameException
from task_management.exceptions.enums import FieldTypes
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
    def create_field(self, create_field_data: CreateFieldDTO) -> FieldDTO:

        self.check_template_exists(template_id=create_field_data.template_id)
        self._validate_user_access_for_template(
            template_id=create_field_data.template_id,
            user_id=create_field_data.created_by)

        self.check_field_name_not_empty(
            field_name=create_field_data.field_name)
        self.check_field_name_not_exist_in_db(
            field_name=create_field_data.field_name,
            template_id=create_field_data.template_id)
        self.check_field_type(field_type=create_field_data.field_type.value)
        self._validate_config(config=create_field_data.config,
                              field_type=create_field_data.field_type.value)

        return self.field_storage.create_field(
            create_field_data=create_field_data)

    @invalidate_interactor_cache(cache_name="field")
    def update_field(self, update_field_data: UpdateFieldDTO,
                     user_id: str) -> FieldDTO:

        is_field_name_provided = update_field_data.field_name is not None
        is_config_provided = update_field_data.config is not None

        self.validate_field_is_active(field_id=update_field_data.field_id)
        field_data = self.field_storage.get_field_by_id(
            field_id=update_field_data.field_id)

        self.check_template_exists(template_id=field_data.template_id)
        self._validate_user_access_for_template(
            template_id=field_data.template_id, user_id=user_id)

        if is_field_name_provided:
            self.check_field_name_not_empty(
                field_name=update_field_data.field_name)
            self.check_field_name_in_db_except_current_field(
                field_id=update_field_data.field_id,
                field_name=update_field_data.field_name,
                template_id=field_data.template_id)

        if is_config_provided:
            self.validate_field_config(field_type=field_data.field_type.value,
                                       config=update_field_data.config)

        is_field_property_provided = any([
            is_field_name_provided,
            is_config_provided,
            update_field_data.description is not None,
            update_field_data.is_required is not None])

        if not is_field_property_provided:
            raise NothingToUpdateFieldException

        return self.field_storage.update_field(
            field_id=update_field_data.field_id,
            update_field_data=update_field_data)

    @invalidate_interactor_cache(cache_name="field")
    def reorder_field(self, field_id: str, template_id: str, new_order: int,
                      user_id: str) -> FieldDTO:

        self.check_template_exists(template_id=template_id)
        self.validate_field_is_active(field_id=field_id)
        self._validate_field_order(template_id=template_id, order=new_order)

        self._validate_user_access_for_template(template_id=template_id,
                                                user_id=user_id)

        return self.field_storage.reorder_fields(
            field_id=field_id, template_id=template_id, new_order=new_order)

    @invalidate_interactor_cache(cache_name="field")
    def delete_field(self, field_id: str, user_id: str) -> FieldDTO:

        self.validate_field_is_active(field_id=field_id)
        field_data = self.field_storage.get_field_by_id(field_id=field_id)

        self._validate_user_access_for_template(
            template_id=field_data.template_id, user_id=user_id)

        return self.field_storage.delete_field(field_id=field_id)

    @interactor_cache(cache_name="field", timeout=5 * 60)
    def get_active_fields_for_template(self, template_id: str) -> list[
        FieldDTO]:

        self.check_template_exists(template_id=template_id)

        return self.field_storage.get_active_fields_for_template(
            template_id=template_id)

    def get_field(self, field_id: str) -> FieldDTO:

        self.validate_field_is_active(field_id=field_id)

        return self.field_storage.get_field_by_id(field_id=field_id)

    def _validate_field_order(self, template_id: str, order: int):
        if order < 1:
            raise InvalidOrderException(order=order)

        fields_count = self.field_storage.template_fields_count(
            template_id=template_id)

        if order > fields_count:
            raise InvalidOrderException(order=order)

    def _validate_user_access_for_template(self, template_id: str,
                                           user_id: str):
        """Validate user has access to workspace containing the template.

        Returns:
            workspace_id for potential further use
        """
        workspace_id = self.template_storage.get_workspace_id_from_template_id(
            template_id=template_id)

        self.validate_user_has_access_to_workspace(
            workspace_id=workspace_id, user_id=user_id)

    @staticmethod
    def _check_dropdown_config(field_type: str, config: dict):
        is_dropdown_field_type = (field_type == FieldTypes.DROPDOWN.value)

        if is_dropdown_field_type and not config:
            raise MissingFieldConfigException(field_type=field_type)

    @staticmethod
    def check_field_name_not_empty(field_name: str):
        is_name_empty = not field_name or not field_name.strip()

        if is_name_empty:
            raise EmptyNameException(name=field_name)

    def _validate_config(self, config: dict, field_type: str):

        self._check_dropdown_config(field_type=field_type, config=config)

        if config:
            self.validate_field_config(field_type=field_type, config=config)
