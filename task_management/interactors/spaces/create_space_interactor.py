from task_management.decorators.caching_decorators import \
    invalidate_interactor_cache
from task_management.interactors.dtos import CreateSpaceDTO, SpaceDTO
from task_management.interactors.storage_interfaces import \
    SpaceStorageInterface, WorkspaceStorageInterface
from task_management.mixins import WorkspaceValidationMixin, \
    SpaceValidationMixin


class CreateSpaceInteractor:

    def __init__(self, space_storage: SpaceStorageInterface,
                 workspace_storage: WorkspaceStorageInterface):
        self.space_storage = space_storage
        self.workspace_storage = workspace_storage

    @property
    def workspace_mixin(self) -> WorkspaceValidationMixin:
        return WorkspaceValidationMixin(
            workspace_storage=self.workspace_storage)

    @property
    def space_mixin(self) -> SpaceValidationMixin:
        return SpaceValidationMixin(space_storage=self.space_storage)

    @invalidate_interactor_cache(cache_name="spaces")
    def create_space(self, space_data: CreateSpaceDTO) -> SpaceDTO:
        self.space_mixin.check_space_name_not_empty(name=space_data.name)
        self.workspace_mixin.check_workspace_not_deleted(
            workspace_id=space_data.workspace_id
        )
        self.workspace_mixin.check_user_has_edit_access_to_workspace(
            user_id=space_data.created_by,
            workspace_id=space_data.workspace_id
        )

        order = self.space_storage.get_last_space_order_in_workspace(
            workspace_id=space_data.workspace_id
        )

        return self.space_storage.create_space(
            space_data=space_data, order=order + 1)
