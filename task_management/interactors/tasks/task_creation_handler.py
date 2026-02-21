from task_management.interactors.dtos import CreateTaskDTO, TaskDTO, \
    CreateFieldValueDTO
from task_management.interactors.storage_interfaces import \
    ListStorageInterface, TaskStorageInterface, \
    WorkspaceStorageInterface, FieldStorageInterface
from task_management.interactors.tasks.task_interactor import TaskInteractor


class TaskCreationHandler:

    def __init__(self, list_storage: ListStorageInterface,
                 task_storage: TaskStorageInterface,
                 workspace_storage: WorkspaceStorageInterface,
                 field_storage: FieldStorageInterface):
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
        task_interactor = TaskInteractor(
            list_storage=self.list_storage,
            task_storage=self.task_storage,
            workspace_storage=self.workspace_storage)

        return task_interactor.create_task(task_data=task_data)

    def _create_default_field_values_at_task(self, task_id: str, list_id: str,
                                             created_by: str):
        template_id = self.list_storage.get_template_id_by_list_id(
            list_id=list_id)
        template_fields = self.field_storage.get_fields_for_template(
            template_id=template_id)

        field_values = []
        for field in template_fields:
            default_value = field.config.get('default')

            field_values.append(
                CreateFieldValueDTO(
                    task_id=task_id,
                    field_id=field.field_id,
                    value=default_value,
                    created_by=created_by
                )
            )

        return self.field_storage.create_bulk_field_values(
            create_bulk_field_values=field_values)
