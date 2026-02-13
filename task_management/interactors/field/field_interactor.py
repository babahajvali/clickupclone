from task_management.exceptions.custom_exceptions import \
    InvalidOrderException, MissingFieldConfigException, \
    NothingToUpdateFieldException
from task_management.exceptions.enums import FieldTypes
from task_management.interactors.dtos import CreateFieldDTO, FieldDTO, \
    UpdateFieldDTO

from task_management.decorators.caching_decorators import interactor_cache, \
    invalidate_interactor_cache
from task_management.interactors.storage_interfaces import \
    FieldStorageInterface, TemplateStorageInterface, ListStorageInterface, \
    SpaceStorageInterface, WorkspaceStorageInterface
from task_management.mixins import TemplateValidationMixin, \
    FieldValidationMixin, ListValidationMixin, WorkspaceValidationMixin


class FieldInteractor(TemplateValidationMixin, WorkspaceValidationMixin,
                      FieldValidationMixin, ListValidationMixin):
    """Field Management Business Logic Interactor.
    
    Handles all field-related operations including creation, updating, deletion,
    reordering, and retrieval of fields within templates. This interactor
    enforces business rules and validates user permissions before performing
    any field operations.
    
    Key Responsibilities:
        - Create new fields with validation
        - Update existing field properties
        - Delete fields with permission checks
        - Reorder fields within templates
        - Retrieve fields for specific templates
        - Validate field configurations and types
    
    Dependencies:
        - FieldStorageInterface: Field data persistence
        - TemplateStorageInterface: Template validation and access
        - WorkspaceMemberStorageInterface: User permission validation
        - ListStorageInterface: List access validation
        - SpaceStorageInterface: Space access validation
    
    Attributes:
        field_storage (FieldStorageInterface): Storage for field operations
        template_storage (TemplateStorageInterface): Storage for template operations
        list_storage (ListStorageInterface): Storage for list operations
        space_storage (SpaceStorageInterface): Storage for space operations
    """

    def __init__(self, field_storage: FieldStorageInterface,
                 template_storage: TemplateStorageInterface,
                 workspace_storage: WorkspaceStorageInterface,
                 list_storage: ListStorageInterface,
                 space_storage: SpaceStorageInterface):
        super().__init__(template_storage=template_storage,
                         workspace_storage=workspace_storage,
                         field_storage=field_storage,
                         list_storage=list_storage)
        self.field_storage = field_storage
        self.template_storage = template_storage
        self.workspace_storage = workspace_storage
        self.list_storage = list_storage
        self.space_storage = space_storage

    @invalidate_interactor_cache(cache_name="fields")
    def create_field(self, create_field_data: CreateFieldDTO) -> FieldDTO:

        self.check_template_exists(template_id=create_field_data.template_id)
        self._validate_user_access_for_template(
            template_id=create_field_data.template_id,
            user_id=create_field_data.created_by)

        self.validate_field_type(field_type=create_field_data.field_type.value)
        self.validate_field_name_not_exists(
            field_name=create_field_data.field_name,
            template_id=create_field_data.template_id)

        if create_field_data.field_type.value == FieldTypes.DROPDOWN.value and not create_field_data.config:
            raise MissingFieldConfigException(
                field_type=create_field_data.field_type.value)

        if create_field_data.config:
            self.validate_field_config(
                field_type=create_field_data.field_type.value,
                config=create_field_data.config)

        return self.field_storage.create_field(
            create_field_data=create_field_data)

    @invalidate_interactor_cache(cache_name="fields")
    def update_field(self, update_field_data: UpdateFieldDTO,
                     user_id: str) -> FieldDTO:

        self.validate_field(field_id=update_field_data.field_id)
        field_data = self.field_storage.get_field_by_id(
            update_field_data.field_id)
        self.validate_field_name_except_current(
            field_id=update_field_data.field_id,
            field_name=update_field_data.field_name,
            template_id=field_data.template_id, )
        self.validate_field_config(field_type=field_data.field_type.value,
                                   config=update_field_data.config)

        self.check_template_exists(template_id=field_data.template_id)
        self._validate_user_access_for_template(
            template_id=field_data.template_id, user_id=user_id)

        has_description_provided = update_field_data.description is not None
        has_field_name_provided = update_field_data.field_name is not None
        has_config_provided = update_field_data.config is not None
        has_is_required_provided = update_field_data.is_required is not None

        fields_to_update = {}

        if has_field_name_provided:
            fields_to_update['field_name'] = update_field_data.field_name
        if has_description_provided:
            fields_to_update['description'] = update_field_data.description
        if has_config_provided:
            fields_to_update['config'] = update_field_data.config
        if has_is_required_provided:
            fields_to_update['is_required'] = update_field_data.is_required

        if not fields_to_update:
            raise NothingToUpdateFieldException

        return self.field_storage.update_field(
            update_field_data=update_field_data)

    @invalidate_interactor_cache(cache_name="fields")
    def reorder_field(self, field_id: str, template_id: str, new_order: int,
                      user_id: str) -> FieldDTO:
        self.validate_field(field_id=field_id)
        self._validate_field_order(template_id=template_id, order=new_order)

        self._validate_user_access_for_template(template_id=template_id,
                                                user_id=user_id)

        return self.field_storage.reorder_fields(
            field_id=field_id, template_id=template_id, new_order=new_order)

    @invalidate_interactor_cache(cache_name="fields")
    def delete_field(self, field_id: str, user_id: str) -> FieldDTO:
        self.validate_field(field_id=field_id)
        field_data = self.field_storage.get_field_by_id(field_id=field_id)

        self._validate_user_access_for_template(
            template_id=field_data.template_id, user_id=user_id)

        return self.field_storage.delete_field(field_id=field_id)

    @interactor_cache(cache_name="fields", timeout=5 * 60)
    def get_fields_for_template(self, list_id: str) -> list[FieldDTO]:
        self.validate_list_is_active(list_id=list_id)
        template_id = self.list_storage.get_template_id_by_list_id(
            list_id=list_id)
        self.check_template_exists(template_id=template_id)

        return self.field_storage.get_fields_for_template(
            template_id=template_id)

    def get_field(self, field_id: str) -> FieldDTO:
        self.validate_field(field_id=field_id)

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
        list_id = self.template_storage.get_template_list_id(
            template_id=template_id)
        space_id = self.list_storage.get_list_space_id(list_id=list_id)
        workspace_id = self.space_storage.get_space_workspace_id(
            space_id=space_id)

        self.validate_user_has_access_to_workspace(
            workspace_id=workspace_id,
            user_id=user_id
        )
