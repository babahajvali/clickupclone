from task_management.interactors.dtos import CreateTemplateDTO, TemplateDTO
from task_management.interactors.storage_interfaces import \
    WorkspaceStorageInterface, TemplateStorageInterface, ListStorageInterface
from task_management.mixins import TemplateValidationMixin, \
    ListValidationMixin, WorkspaceValidationMixin


class CreateTemplateInteractor:
    def __init__(
            self, workspace_storage: WorkspaceStorageInterface,
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

    def create_template(self, template_data: CreateTemplateDTO) -> TemplateDTO:
        self.template_mixin.check_template_name_not_empty(
            template_name=template_data.name)
        self.list_mixin.check_list_not_deleted(
            list_id=template_data.list_id)
        self._check_user_has_edit_access_for_list(
            list_id=template_data.list_id, user_id=template_data.created_by)

        return self.template_storage.create_template(template_data)

    def _check_user_has_edit_access_for_list(self, list_id: str, user_id: str):
        workspace_id = self.list_storage.get_workspace_id_by_list_id(
            list_id=list_id)
        self.workspace_mixin.check_user_has_edit_access_to_workspace(
            workspace_id=workspace_id, user_id=user_id)
