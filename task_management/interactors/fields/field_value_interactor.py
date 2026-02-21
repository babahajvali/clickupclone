from task_management.interactors.dtos import TaskFieldValueDTO, \
    UpdateFieldValueDTO
from task_management.interactors.fields.validators.field_value_validator \
    import FieldValueValidator
from task_management.interactors.storage_interfaces import \
    FieldStorageInterface, TaskStorageInterface, WorkspaceStorageInterface
from task_management.mixins import FieldValidationMixin, \
    WorkspaceValidationMixin, TaskValidationMixin


class FieldValueInteractor:

    def __init__(self,
                 field_storage: FieldStorageInterface,
                 task_storage: TaskStorageInterface,
                 workspace_storage: WorkspaceStorageInterface):
        self.field_storage = field_storage
        self.task_storage = task_storage
        self.workspace_storage = workspace_storage

    @property
    def field_mixin(self) -> FieldValidationMixin:
        return FieldValidationMixin(field_storage=self.field_storage)

    @property
    def task_mixin(self) -> TaskValidationMixin:
        return TaskValidationMixin(task_storage=self.task_storage)

    @property
    def field_value_validator(self):
        return FieldValueValidator()

    @property
    def workspace_mixin(self) -> WorkspaceValidationMixin:
        return WorkspaceValidationMixin(
            workspace_storage=self.workspace_storage)

    def set_task_field_value(
            self, set_value_data: UpdateFieldValueDTO, user_id: str) \
            -> TaskFieldValueDTO:
        self.task_mixin.check_task_is_active(task_id=set_value_data.task_id)
        self.field_mixin.check_field_is_active(
            field_id=set_value_data.field_id
        )

        field_data = self.field_storage.get_field_by_id(
            field_id=set_value_data.field_id
        )
        self.field_value_validator.validate_field_value(
            config=field_data.config,
            value=set_value_data.value,
            field_type=field_data.field_type.value
        )
        self._check_user_has_edit_access_for_field(
            field_id=set_value_data.field_id, user_id=user_id
        )

        return self.field_storage.update_or_create_task_field_value(
            field_value_data=set_value_data, user_id=user_id)

    def _check_user_has_edit_access_for_field(
            self, field_id: str, user_id: str):
        workspace_id = self.field_storage.get_workspace_id_from_field_id(
            field_id=field_id)

        self.workspace_mixin.check_user_has_access_to_workspace(
            workspace_id=workspace_id, user_id=user_id
        )
