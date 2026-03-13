from typing import Optional

from task_management.exceptions.custom_exceptions import \
    NothingToUpdateTemplate
from task_management.interactors.dtos import TemplateDTO
from task_management.interactors.storage_interfaces import \
    WorkspaceStorageInterface, TemplateStorageInterface
from task_management.mixins import TemplateValidationMixin, \
    WorkspaceValidationMixin


class UpdateTemplateInteractor(
    TemplateValidationMixin,
    WorkspaceValidationMixin):

    def __init__(
            self, workspace_storage: WorkspaceStorageInterface,
            template_storage: TemplateStorageInterface):
        super().__init__(
            workspace_storage=workspace_storage,
            template_storage=template_storage,
        )
        self.workspace_storage = workspace_storage
        self.template_storage = template_storage

    def update_template(
            self, template_id: str, user_id: str, name: Optional[str],
            description: Optional[str]) -> TemplateDTO:

        self._check_template_update_field_properties(
            template_id=template_id, name=name, description=description)
        self.check_template_exists(template_id=template_id)
        self._check_user_has_edit_access_for_template(
            template_id=template_id, user_id=user_id)

        return self.template_storage.update_template(
            template_id=template_id, name=name, description=description)

    def _check_user_has_edit_access_for_template(
            self, template_id: str, user_id: str):

        workspace_id = self.template_storage.get_workspace_id_from_template_id(
            template_id=template_id)
        self.check_user_has_edit_access_to_workspace(
            workspace_id=workspace_id, user_id=user_id)

    def _check_template_update_field_properties(
            self, template_id: str, name: Optional[str],
            description: Optional[str]):

        is_name_provided = name is not None
        is_description_provided = description is not None

        has_no_update_template_properties = not (
                is_description_provided or is_name_provided)

        if has_no_update_template_properties:
            raise NothingToUpdateTemplate(template_id=template_id)

        if is_name_provided:
            self.check_template_name_not_empty(
                template_name=name)
