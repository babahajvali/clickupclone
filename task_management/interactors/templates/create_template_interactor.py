from task_management.interactors.dtos import CreateTemplateDTO, TemplateDTO
from task_management.interactors.storage_interfaces import \
    WorkspaceStorageInterface, TemplateStorageInterface, ListStorageInterface
from task_management.mixins import TemplateValidationMixin, \
    ListValidationMixin, WorkspaceValidationMixin


class CreateTemplateInteractor(
    TemplateValidationMixin,
    ListValidationMixin,
    WorkspaceValidationMixin):
    def __init__(
            self, workspace_storage: WorkspaceStorageInterface,
            template_storage: TemplateStorageInterface,
            list_storage: ListStorageInterface):
        super().__init__(
            workspace_storage=workspace_storage,
            template_storage=template_storage,
            list_storage=list_storage,
        )
        self.workspace_storage = workspace_storage
        self.template_storage = template_storage
        self.list_storage = list_storage

    def create_template(
            self, create_template_dto: CreateTemplateDTO) -> TemplateDTO:
        self.check_template_name_not_empty(
            template_name=create_template_dto.name)
        self.check_list_not_deleted(
            list_id=create_template_dto.list_id)
        self._check_user_has_edit_access_for_list(
            list_id=create_template_dto.list_id,
            user_id=create_template_dto.created_by,
        )

        return self.template_storage.create_template(
            create_template_dto=create_template_dto)

    def _check_user_has_edit_access_for_list(
            self, list_id: str, user_id: str) -> None:
        workspace_id = self.list_storage.get_workspace_id_by_list_id(
            list_id=list_id)
        self.check_user_has_edit_access_to_workspace(
            workspace_id=workspace_id, user_id=user_id)
