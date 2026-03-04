from task_management.exceptions.enums import FieldType
from task_management.interactors.dtos import TaskFieldValueDTO, \
    UpdateFieldValueDTO

from task_management.interactors.fields.validators.dropdown_validator import \
    DropdownField
from task_management.interactors.fields.validators.number_validator import \
    NumberField
from task_management.interactors.fields.validators.text_validator import \
    TextField
from task_management.interactors.storage_interfaces import \
    FieldStorageInterface, TaskStorageInterface, WorkspaceStorageInterface
from task_management.mixins import FieldValidationMixin, \
    WorkspaceValidationMixin, TaskValidationMixin


class FieldResponseInteractor:
    """
    Field Response Interactor set or update the task field value

    Handle the task field value operation.
    This interactor check the business logic and permission validation
     before set the task field value.

    Key Responsibility:
     - Create or update the task field value with validations

    Dependencies:
        - FieldStorageInterface
        - TaskStorageInterface
        - WorkspaceStorageInterface

    """

    def __init__(
            self, field_storage: FieldStorageInterface,
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
    def workspace_mixin(self) -> WorkspaceValidationMixin:
        return WorkspaceValidationMixin(
            workspace_storage=self.workspace_storage)

    def set_task_field_response(
            self, set_value_data: UpdateFieldValueDTO, user_id: str) \
            -> TaskFieldValueDTO:
        """Set or update a task's value for a specific custom field."""
        self.task_mixin.check_task_not_deleted(
            task_id=set_value_data.task_id)
        self.field_mixin.check_field_not_deleted(
            field_id=set_value_data.field_id
        )
        self._check_user_has_edit_access_for_field(
            field_id=set_value_data.field_id, user_id=user_id
        )
        field_data = self.field_storage.get_field(
            field_id=set_value_data.field_id
        )
        self._check_field_value_by_type(
            config=field_data.config,
            value=set_value_data.value,
            field_type=field_data.field_type.value
        )

        return self.field_storage.update_or_create_task_field_value(
            field_value_data=set_value_data, user_id=user_id)

    def _check_user_has_edit_access_for_field(
            self, field_id: str, user_id: str):
        workspace_id = self.field_storage.get_workspace_id_from_field_id(
            field_id=field_id)

        self.workspace_mixin.check_user_has_edit_access_to_workspace(
            workspace_id=workspace_id, user_id=user_id
        )

    @staticmethod
    def _check_field_value_by_type(field_type: str, value: str, config: dict):
        validation_handlers = {
            FieldType.TEXT.value:
                TextField.check_text_value_not_exceeds_max_length,
            FieldType.NUMBER.value: NumberField.check_number_value_within_range,
            FieldType.DROPDOWN.value: DropdownField.check_dropdown_value_in_options,
        }

        handler = validation_handlers.get(field_type)
        if handler:
            handler(value=value, config=config)
