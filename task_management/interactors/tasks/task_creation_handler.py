from task_management.exceptions.enums import FieldConfig
from task_management.interactors.dtos import CreateTaskDTO, TaskDTO, \
    CreateFieldValueDTO
from task_management.interactors.storage_interfaces import \
    ListStorageInterface, TaskStorageInterface, \
    WorkspaceStorageInterface, FieldStorageInterface
from task_management.interactors.tasks.create_task_interactor import \
    CreateTaskInteractor


class TaskCreationHandler:

    def __init__(
            self, list_storage: ListStorageInterface,
            task_storage: TaskStorageInterface,
            workspace_storage: WorkspaceStorageInterface,
            field_storage: FieldStorageInterface
    ):
        self.list_storage = list_storage
        self.task_storage = task_storage
        self.workspace_storage = workspace_storage
        self.field_storage = field_storage

    def handle_task_creation(self, task_data: CreateTaskDTO) -> TaskDTO:
        task = self._create_task(task_data=task_data)

        self._create_default_field_values_at_task(
            task_id=task.task_id, list_id=task.list_id,
            created_by=task.created_by)

        return task

    def _create_task(self, task_data: CreateTaskDTO) -> TaskDTO:
        task_interactor = CreateTaskInteractor(
            list_storage=self.list_storage,
            task_storage=self.task_storage,
            workspace_storage=self.workspace_storage)

        return task_interactor.create_task(task_data=task_data)

    def _create_default_field_values_at_task(
            self, task_id: str, list_id: str, created_by: str):
        template_fields = self._get_template_fields_by_list_id(list_id=list_id)
        field_values = self._build_default_field_values(
            task_id=task_id,
            created_by=created_by,
            template_fields=template_fields
        )
        return self.field_storage.create_bulk_field_values(
            create_bulk_field_values=field_values)

    def _get_template_fields_by_list_id(self, list_id: str):
        template_id = self.list_storage.get_template_id_by_list_id(
            list_id=list_id)
        return self.field_storage.get_fields_for_template(
            template_id=template_id)

    @staticmethod
    def _build_default_field_values(
            task_id: str, created_by: str, template_fields: list):
        return [
            CreateFieldValueDTO(
                task_id=task_id,
                field_id=field.field_id,
                value=field.config.get(FieldConfig.DEFAULT.value),
                created_by=created_by
            )
            for field in template_fields
        ]
