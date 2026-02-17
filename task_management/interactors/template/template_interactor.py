from typing import Optional

from task_management.exceptions.custom_exceptions import EmptyNameException, \
    NothingToUpdateTemplateException
from task_management.interactors.dtos import CreateTemplateDTO, TemplateDTO
from task_management.interactors.storage_interfaces import \
    WorkspaceStorageInterface, TemplateStorageInterface, ListStorageInterface
from task_management.mixins import TemplateValidationMixin, \
    ListValidationMixin, WorkspaceValidationMixin


class TemplateInteractor(TemplateValidationMixin, ListValidationMixin,
                         WorkspaceValidationMixin):
    """Template Management Business Logic Interactor.
    
    Handles all template-related operations including creation, updating, and
    retrieval of templates within lists. This interactor enforces business
    rules and validates user permissions before performing any template operations.
    
    Key Responsibilities:
        - Create new templates with validation
        - Update existing template properties
        - Validate template names and descriptions
        - Ensure user has proper workspace access
        - Manage template-field relationships
    
    Dependencies:
        - FieldStorageInterface: Field operations for template validation
        - WorkspaceMemberStorageInterface: User permission validation
        - TemplateStorageInterface: Template data persistence
        - ListStorageInterface: List access validation
        - SpaceStorageInterface: Space access validation
    
    Attributes:
        template_storage (TemplateStorageInterface): Storage for template operations
        list_storage (ListStorageInterface): Storage for list operations
    """

    def __init__(self, workspace_storage: WorkspaceStorageInterface,
                 template_storage: TemplateStorageInterface,
                 list_storage: ListStorageInterface):
        super().__init__(template_storage=template_storage,
                         list_storage=list_storage,
                         workspace_storage=workspace_storage)
        self.workspace_storage = workspace_storage
        self.template_storage = template_storage
        self.list_storage = list_storage

    def create_template(self, template_data: CreateTemplateDTO) -> TemplateDTO:

        self._validate_template_name_not_empty(
            template_name=template_data.name)
        self.validate_list_is_active(list_id=template_data.list_id)
        self._validate_user_access_for_list(list_id=template_data.list_id,
                                            user_id=template_data.created_by)


        result = self.template_storage.create_template(template_data)

        return result

    def update_template(
            self, template_id: str, user_id: str, name: Optional[str],
            description: Optional[str]) -> TemplateDTO:

        self.check_template_exists(template_id=template_id)
        template_data = self.template_storage.get_template_by_id(
            template_id=template_id)
        self._validate_user_access_for_list(list_id=template_data.list_id,
                                            user_id=user_id)

        is_name_provided = name is not None
        is_description_provided = description is not None

        fields_to_update = {}

        if is_name_provided:
            self._validate_template_name_not_empty(template_name=name)
            fields_to_update["name"] = name

        if is_description_provided:
            fields_to_update["description"] = description

        if not fields_to_update:
            raise NothingToUpdateTemplateException(template_id=template_id)

        return self.template_storage.update_template(template_id=template_id,
                                                     update_fields=fields_to_update)

    def _validate_user_access_for_list(self, list_id: str, user_id: str):

        workspace_id = self.list_storage.get_workspace_id_by_list_id(
            list_id=list_id)
        self.validate_user_has_access_to_workspace(
            workspace_id=workspace_id, user_id=user_id)

    @staticmethod
    def _validate_template_name_not_empty(template_name: str):
        if not template_name or not template_name.strip():
            raise EmptyNameException(name=template_name)
