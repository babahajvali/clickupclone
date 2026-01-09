from django.db.models import F

from task_management.interactors.dtos import CreateTaskDTO, TaskDTO, \
    UpdateTaskDTO, FilterDTO
from task_management.interactors.storage_interface.task_storage_interface import \
    TaskStorageInterface
from task_management.models import User, List, Task


class TaskStorage(TaskStorageInterface):
    @staticmethod
    def _task_dto(task_data: Task) -> TaskDTO:
        return TaskDTO(
            task_id=task_data.task_id,
            title=task_data.title,
            description=task_data.description,
            order=task_data.order,
            is_delete=task_data.is_deleted,
            created_by=task_data.created_by,
            list_id=task_data.list.list_id,
        )

    def create_task(self, task_data: CreateTaskDTO) -> TaskDTO:
        user = User.objects.get(user_id=task_data.created_by)
        list_obj = List.objects.get(list_id=task_data.list_id)
        last_task = Task.objects.filter(
            list_id=task_data.list_id, is_deleted=False).order_by(
            '-order').first()
        next_order = (last_task.order + 1) if last_task else 1

        task_data = Task.objects.create(
            title=task_data.title, description=task_data.description,
            list=list_obj, created_by=user, order=next_order)

        return self._task_dto(task_data=task_data)

    def update_task(self, update_task_data: UpdateTaskDTO) -> TaskDTO:
        task_data = Task.objects.get(task_id=update_task_data.task_id)
        if update_task_data.title:
            task_data.title = update_task_data.title

        if update_task_data.description:
            task_data.description = update_task_data.description

        task_data.save()
        return self._task_dto(task_data=task_data)

    def get_task_by_id(self, task_id: str) -> TaskDTO:
        task_data = Task.objects.get(task_id=task_id)

        return self._task_dto(task_data=task_data)

    def get_list_tasks(self, list_id: str) -> list[TaskDTO]:
        list_tasks = Task.objects.filter(list_id=list_id, is_deleted=False)

        return [self._task_dto(task_data=task_data) for task_data in
                list_tasks]

    def remove_task(self, task_id: str) -> TaskDTO:
        task_data = Task.objects.get(task_id=task_id)
        task_data.is_deleted = True
        task_data.save()
        current_order = task_data.order
        Task.objects.filter(
            list_id=task_data.list.list_id, is_deleted=False,
            order__gt=current_order).update(order=F("order") - 1)

        return self._task_dto(task_data=task_data)

    def task_filter_data(self, filter_data: FilterDTO):
        active_tasks = Task.objects.filter(list_id=filter_data.list_id,
                                           is_deleted=False).prefetch_related(
            "taskassignee_set",
            "task_field_values",
        )

        if filter_data.assignees:
            active_tasks = active_tasks.filter(
                taskassignee__user_id__in=filter_data.assignees,
                taskassignee__is_active=True
            )

        if filter_data.field_filters:
            for field_id, values in filter_data.field_filters.items():
                active_tasks = active_tasks.filter(
                    task_field_values__field_id=field_id,
                    task_field_values__value__in=values
                )

        active_tasks = active_tasks.distinct().order_by('order')

        return active_tasks[
            filter_data.offset: filter_data.offset + filter_data.limit]

    def get_tasks_count(self, list_id: str):
        return Task.objects.filter(list_id=list_id, is_deleted=False).count()

    def reorder_tasks(self, list_id: str, order: int, task_id: str):
        new_order = order
        task_data = Task.objects.get(task_id=task_id)
        old_order = task_data.order

        if old_order == new_order:
            return self._task_dto(task_data=task_data)

        if new_order > old_order:
            Task.objects.filter(
                list_id=list_id, is_deleted=False, order__gt=old_order,
                order__lte=new_order).update(order=F("order") - 1)

        else:
            Task.objects.filter(
                list_id=list_id, is_deleted=False, order__gte=new_order,
                order__lt=old_order).update(order=F("order") + 1)

        task_data.order = new_order
        task_data.save()

        return self._task_dto(task_data=task_data)
