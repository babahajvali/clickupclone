from django.db import transaction

from task_management.decorators.caching_decorators import \
    invalidate_interactor_cache
from task_management.exceptions.custom_exceptions import InvalidOrder
from task_management.interactors.dtos import FolderDTO
from task_management.interactors.folders.validators.folder_validator import \
    FolderValidator
from task_management.interactors.storage_interfaces import \
    FolderStorageInterface, WorkspaceStorageInterface, SpaceStorageInterface
from task_management.mixins import FolderValidationMixin, SpaceValidationMixin, \
    WorkspaceValidationMixin


class ReorderFolderInteractor:

    def __init__(self, folder_storage: FolderStorageInterface,
                 workspace_storage: WorkspaceStorageInterface,
                 space_storage: SpaceStorageInterface):
        self.folder_storage = folder_storage
        self.workspace_storage = workspace_storage
        self.space_storage = space_storage

    @property
    def folder_mixin(self) -> FolderValidationMixin:
        return FolderValidationMixin(folder_storage=self.folder_storage)

    @property
    def space_mixin(self) -> SpaceValidationMixin:
        return SpaceValidationMixin(space_storage=self.space_storage)

    @property
    def workspace_mixin(self) -> WorkspaceValidationMixin:
        return WorkspaceValidationMixin(
            workspace_storage=self.workspace_storage)

    @property
    def folder_validator(self) -> FolderValidator:
        return FolderValidator(folder_storage=self.folder_storage)

    @transaction.atomic
    @invalidate_interactor_cache(cache_name="folders")
    def reorder_folder(
            self, space_id: str, folder_id: str, user_id: str, order: int) \
            -> FolderDTO:
        self._check_folder_order(
            space_id=space_id, order=order
        )
        self.folder_mixin.check_folder_not_deleted(folder_id=folder_id)
        self.space_mixin.check_space_not_deleted(space_id=space_id)
        self._check_user_has_edit_access_for_space(
            space_id=space_id, user_id=user_id
        )

        folder_data = self.folder_storage.get_folder(folder_id=folder_id)
        old_order = folder_data.order

        if old_order == order:
            return folder_data

        return self._reorder_folder_positions(
            space_id=space_id, old_order=old_order, new_order=order,
            folder_id=folder_id)

    def _check_user_has_edit_access_for_space(
            self, space_id: str, user_id: str):
        workspace_id = self.space_storage.get_space_workspace_id(
            space_id=space_id)

        self.workspace_mixin.check_user_has_edit_access_to_workspace(
            user_id=user_id, workspace_id=workspace_id
        )

    def _check_folder_order(self, space_id: str, order: int):
        if order < 1:
            raise InvalidOrder(order=order)
        folder_count = self.folder_storage.get_space_folder_count(
            space_id=space_id)

        if order > folder_count:
            raise InvalidOrder(order=order)

    def _reorder_folder_positions(self, space_id: str, old_order: int,
                                  new_order: int, folder_id: str):
        self._reorder_folder_positions_except_current(
            space_id=space_id, old_order=old_order, new_order=new_order
        )

        return self.folder_storage.update_folder_order(
            folder_id=folder_id, new_order=new_order)

    def _reorder_folder_positions_except_current(
            self, space_id: str, old_order: int, new_order: int):

        if new_order > old_order:
            self.folder_storage.shift_folders_down(
                space_id=space_id, old_order=old_order, new_order=new_order
            )
        else:
            self.folder_storage.shift_folders_up(
                space_id=space_id, old_order=old_order, new_order=new_order
            )
