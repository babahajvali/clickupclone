from task_management.decorators.caching_decorators import \
    invalidate_interactor_cache
from task_management.interactors.dtos import CreateSpaceDTO, SpaceDTO
from task_management.interactors.storage_interfaces import \
    SpaceStorageInterface, WorkspaceStorageInterface
from task_management.mixins import WorkspaceValidationMixin, \
    SpaceValidationMixin


class CreateSpaceInteractor(WorkspaceValidationMixin, SpaceValidationMixin):

    def __init__(
            self, space_storage: SpaceStorageInterface,
            workspace_storage: WorkspaceStorageInterface):
        super().__init__(workspace_storage=workspace_storage,
                         space_storage=space_storage)
        self.space_storage = space_storage
        self.workspace_storage = workspace_storage

    @invalidate_interactor_cache(cache_name="spaces")
    def create_space(self, space_data: CreateSpaceDTO) -> SpaceDTO:
        self.check_space_name_not_empty(name=space_data.name)
        self.check_workspace_not_deleted(
            workspace_id=space_data.workspace_id
        )
        self.check_user_has_edit_access_to_workspace(
            user_id=space_data.created_by,
            workspace_id=space_data.workspace_id
        )

        last_space_order_in_workspace = (
            self.space_storage.get_last_space_order_in_workspace(
                workspace_id=space_data.workspace_id))

        return self.space_storage.create_space(
            space_data=space_data, order=last_space_order_in_workspace + 1)
