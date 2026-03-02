from typing import Optional

from task_management.decorators.caching_decorators import \
    invalidate_interactor_cache
from task_management.interactors.dtos import TaskDTO
from task_management.interactors.storage_interfaces import \
    TaskStorageInterface, WorkspaceStorageInterface
from task_management.interactors.tasks.validators.task_validator import \
    TaskValidator
from task_management.mixins import TaskValidationMixin, \
    WorkspaceValidationMixin


class UpdateTaskInteractor:

    def __init__(self, task_storage: TaskStorageInterface,
                 workspace_storage: WorkspaceStorageInterface):
        self.task_storage = task_storage
        self.workspace_storage = workspace_storage

    @property
    def task_mixin(self) -> TaskValidationMixin:
        return TaskValidationMixin(task_storage=self.task_storage)

    @property
    def workspace_mixin(self) -> WorkspaceValidationMixin:
        return WorkspaceValidationMixin(
            workspace_storage=self.workspace_storage)

    @property
    def task_validator(self) -> TaskValidator:
        return TaskValidator(task_storage=self.task_storage)

    @invalidate_interactor_cache(cache_name="tasks")
    def update_task(
            self, task_id: str, user_id: str, title: Optional[str],
            description: Optional[str]) -> TaskDTO:
        self._check_task_update_field_properties(
            task_id=task_id, title=title, description=description)
        self.task_mixin.check_task_not_deleted(task_id=task_id)
        self._check_user_has_edit_access_for_task(
            task_id=task_id, user_id=user_id)

        return self.task_storage.update_task(
            task_id=task_id, title=title, description=description)

    def _check_user_has_edit_access_for_task(self, task_id: str, user_id: str):
        workspace_id = self.task_storage.get_workspace_id_from_task_id(
            task_id=task_id)

        self.workspace_mixin.check_user_has_edit_access_to_workspace(
            workspace_id=workspace_id, user_id=user_id)

    def _check_task_update_field_properties(
            self, task_id: str, title: Optional[str],
            description: Optional[str]):
        from task_management.exceptions.custom_exceptions import \
            NothingToUpdateTask

        is_title_provided = title is not None
        is_description_provided = description is not None
        is_no_update_field_properties_provided = any([
            is_description_provided,
            is_title_provided
        ])

        if not is_no_update_field_properties_provided:
            raise NothingToUpdateTask(task_id=task_id)
        if is_title_provided:
            self.task_validator.check_task_title_not_empty(title=title)
