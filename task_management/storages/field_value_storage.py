from task_management.interactors.dtos import UpdateFieldValueDTO, \
    TaskFieldValueDTO, TaskFieldValuesDTO, FieldValueDTO, CreateFieldValueDTO
from task_management.interactors.storage_interfaces.task_field_values_storage_interface import \
    FieldValueStorageInterface
from task_management.models import FieldValue, Task, Field, User


class FieldValueStorage(FieldValueStorageInterface):

    def set_task_field_value(self, field_value_data: UpdateFieldValueDTO) -> \
            TaskFieldValueDTO:
        field_value_data_obj = FieldValue.objects.get(
            task_id=field_value_data.task_id,
            field_id=field_value_data.field_id)
        field_value_data_obj.value = field_value_data.value
        field_value_data_obj.save()

        return TaskFieldValueDTO(
            id=field_value_data_obj.pk,
            task_id=field_value_data_obj.task.task_id,
            field_id=field_value_data_obj.field.field_id,
            value=field_value_data_obj.value,
        )

    def get_field_values_by_task_ids(self, task_ids: list[str]) -> list[
        TaskFieldValuesDTO]:
        field_values = FieldValue.objects.filter(
            task_id__in=task_ids
        ).select_related('field', 'task')

        task_values_map = {}
        for fv in field_values:
            if fv.value is None:
                continue
            task_id = str(fv.task.task_id)
            if task_id not in task_values_map:
                task_values_map[task_id] = []

            task_values_map[task_id].append(
                FieldValueDTO(
                    field_id=fv.field.field_id,
                    value=fv.value
                )
            )
        result = []
        for task_id in task_ids:
            result.append(
                TaskFieldValuesDTO(
                    task_id=task_id,
                    values=task_values_map.get(task_id, [])
                )
            )
        return result

    def create_bulk_field_values(self,
                                 create_bulk_field_values: list[CreateFieldValueDTO]):
        task_ids = [fv.task_id for fv in create_bulk_field_values]
        field_ids = [fv.field_id for fv in create_bulk_field_values]
        user_ids = [fv.created_by for fv in create_bulk_field_values]

        tasks = {str(t.task_id): t for t in
                 Task.objects.filter(task_id__in=task_ids)}
        fields = {str(f.field_id): f for f in
                  Field.objects.filter(field_id__in=field_ids)}
        users = {str(u.user_id): u for u in
                 User.objects.filter(user_id__in=user_ids)}

        field_values_to_create = []
        for fv_data in create_bulk_field_values:
            task = tasks[str(fv_data.task_id)]
            field = fields[str(fv_data.field_id)]
            created_by = users[str(fv_data.created_by)]
            field_values_to_create.append(
                FieldValue(
                    task=task,
                    field=field,
                    value=fv_data.value,
                    created_by=created_by
                )
            )

        FieldValue.objects.bulk_create(field_values_to_create)

    def check_task_field_value(self,task_id: str, field_id: str) -> bool:
        return FieldValue.objects.filter(task_id=task_id, field_id=field_id).exists()

