from typing import Optional

from task_management.exceptions.custom_exceptions import \
    NothingToUpdateTemplate
from task_management.interactors.dtos import TemplateDTO
from task_management.interactors.storage_interfaces import \
    WorkspaceStorageInterface, TemplateStorageInterface, ListStorageInterface
from task_management.mixins import TemplateValidationMixin, \
    ListValidationMixin, WorkspaceValidationMixin


class TemplateInteractor:
    """Template Management Business Logic Interactor.
    
    Handles all templates-related operations including creation, updating, and
    retrieval of templates within lists. This interactor enforces business
    rules and validates user permissions before performing any templates operations.
    
    Key Responsibilities:
        - Create new templates with validation
        - Update existing templates properties
        - Validate templates names and descriptions
        - Ensure user has proper workspaces access
        - Manage templates-fields relationships
    
    Dependencies:
        - FieldStorageInterface: Field operations for templates validation
        - WorkspaceMemberStorageInterface: User permission validation
        - TemplateStorageInterface: Template data persistence
        - ListStorageInterface: List access validation
        - SpaceStorageInterface: Space access validation
    
    Attributes:
        template_storage (TemplateStorageInterface): Storage for templates operations
        list_storage (ListStorageInterface): Storage for lists operations
    """

    def __init__(self, workspace_storage: WorkspaceStorageInterface,
                 template_storage: TemplateStorageInterface,
                 list_storage: ListStorageInterface):

        self.workspace_storage = workspace_storage
        self.template_storage = template_storage
        self.list_storage = list_storage

    @property
    def template_mixin(self) -> TemplateValidationMixin:
        return TemplateValidationMixin(template_storage=self.template_storage)

    @property
    def list_mixin(self) -> ListValidationMixin:
        return ListValidationMixin(list_storage=self.list_storage)

    @property
    def workspace_mixin(self) -> WorkspaceValidationMixin:
        return WorkspaceValidationMixin(
            workspace_storage=self.workspace_storage)

    def update_template(
            self, template_id: str, user_id: str, name: Optional[str],
            description: Optional[str]) -> TemplateDTO:

        self._check_template_update_field_properties(
            template_id=template_id, name=name, description=description)
        self.template_mixin.check_template_exists(template_id=template_id)
        list_id = self.template_storage.get_template_list_id(
            template_id=template_id)
        self._check_user_has_edit_access_for_list(
            list_id=list_id,
            user_id=user_id)

        return self.template_storage.update_template(
            template_id=template_id, name=name, description=description)

    def _check_user_has_edit_access_for_list(self, list_id: str, user_id: str):

        workspace_id = self.list_storage.get_workspace_id_by_list_id(
            list_id=list_id)
        self.workspace_mixin.check_user_has_edit_access_to_workspace(
            workspace_id=workspace_id, user_id=user_id)

    def _check_template_update_field_properties(
            self, template_id: str, name: Optional[str],
            description: Optional[str]):

        is_name_provided = name is not None
        is_description_provided = description is not None

        has_no_update_field_properties = not any([
            is_name_provided,
            is_description_provided
        ])

        if has_no_update_field_properties:
            raise NothingToUpdateTemplate(template_id=template_id)

        if is_name_provided:
            self.template_mixin.check_template_name_not_empty(
                template_name=name)
