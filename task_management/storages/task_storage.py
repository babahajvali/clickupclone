from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F

from task_management.interactors.dtos import CreateTaskDTO, TaskDTO, \
    FilterDTO, TaskAssigneeDTO, UserTasksDTO
from task_management.interactors.storage_interfaces.task_storage_interface import \
    TaskStorageInterface
from task_management.models import User, List, Task, TaskAssignee


class TaskStorage(TaskStorageInterface):
    @staticmethod
    def _task_dto(task_data: Task) -> TaskDTO:
        return TaskDTO(
            task_id=task_data.task_id,
            title=task_data.title,
            description=task_data.description,
            order=task_data.order,
            is_deleted=task_data.is_deleted,
            created_by=task_data.created_by.user_id,
            list_id=task_data.list.list_id,
        )

    @staticmethod
    def _assignee_dto(assignee_data: TaskAssignee) -> TaskAssigneeDTO:
        return TaskAssigneeDTO(
            assign_id=assignee_data.assign_id,
            task_id=assignee_data.task.task_id,
            user_id=assignee_data.user.user_id,
            is_active=assignee_data.is_active,
            assigned_by=assignee_data.assigned_by.user_id,
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

    def update_task(self, task_id: str, field_properties: dict) -> TaskDTO:
        Task.objects.filter(task_id=task_id).update(**field_properties)

        task_data = Task.objects.get(task_id=task_id)

        return self._task_dto(task_data=task_data)

    def get_task_by_id(self, task_id: str) -> TaskDTO:
        task_data = Task.objects.get(task_id=task_id)

        return self._task_dto(task_data=task_data)

    def get_task_list_id(self, task_id: str) -> str:

        task = Task.objects.select_related('list').get(task_id=task_id)
        return task.list.list_id

    def get_workspace_id_from_task_id(self, task_id: str) -> str | None:
        try:
            task_data = Task.objects.get(task_id=task_id)

            return task_data.list.space.workspace.workspace_id
        except ObjectDoesNotExist:
            return None

    def get_active_tasks_for_list(self, list_id: str) -> list[TaskDTO]:
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
        active_tasks = Task.objects.filter(
            list_id=filter_data.list_id, is_deleted=False).prefetch_related(
            "task_assignees", "task_field_values",
        )

        if filter_data.assignees:
            active_tasks = active_tasks.filter(
                task_assignees__user_id__in=filter_data.assignees,
                task_assignees__is_active=True
            )

        if filter_data.field_filters:
            for field_id, values in filter_data.field_filters.items():
                active_tasks = active_tasks.filter(
                    task_field_values__field_id=field_id,
                    task_field_values__value__in=values
                )

        active_tasks = active_tasks.distinct().order_by('order')

        return active_tasks[
            filter_data.offset - 1: filter_data.offset - 1 + filter_data.limit]

    def get_tasks_count(self, list_id: str) -> int:
        return Task.objects.filter(list_id=list_id, is_deleted=False).count()

    def reorder_tasks(self, list_id: str, new_order: int,
                      task_id: str) -> TaskDTO:
        task_data = Task.objects.get(task_id=task_id)
        old_order = task_data.order

        if old_order == new_order:
            return self._task_dto(task_data=task_data)

        task_data.order = 0
        task_data.save()
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

    def assign_task_assignee(self, task_id: str, user_id: str,
                             assigned_by: str) -> TaskAssigneeDTO:
        user = User.objects.get(user_id=user_id)
        task = Task.objects.get(task_id=task_id)
        assigned_by = User.objects.get(user_id=assigned_by)

        assignment_data = TaskAssignee.objects.create(assigned_by=assigned_by,
                                                      task=task, user=user)

        return self._assignee_dto(assignee_data=assignment_data)

    def remove_task_assignee(self, assign_id: str) -> TaskAssigneeDTO:
        assignee_data = TaskAssignee.objects.get(assign_id=assign_id)
        assignee_data.is_active = False
        assignee_data.save()

        return self._assignee_dto(assignee_data=assignee_data)

    def get_task_assignee(self, assign_id: str) -> TaskAssigneeDTO:
        assignee_data = TaskAssignee.objects.get(assign_id=assign_id)

        return self._assignee_dto(assignee_data=assignee_data)

    def get_task_assignees(self, task_id: str) -> list[TaskAssigneeDTO]:
        task_assignees = TaskAssignee.objects.filter(task_id=task_id,
                                                     is_active=True)

        return [self._assignee_dto(assignee_data=data) for data in
                task_assignees]

    def get_user_assigned_tasks(self, user_id: str) -> UserTasksDTO:
        assignees = TaskAssignee.objects.filter(
            user_id=user_id, is_active=True, task__is_deleted=False)

        tasks = []
        for assignee in assignees:
            tasks.append(TaskDTO(
                task_id=str(assignee.task.task_id),
                title=assignee.task.title,
                description=assignee.task.description,
                list_id=str(assignee.task.list.list_id),
                order=assignee.task.order,
                created_by=str(assignee.task.created_by_user_id.user_id),
                is_deleted=assignee.task.is_deleted
            ))

        return UserTasksDTO(
            user_id=user_id,
            tasks=tasks
        )

    def get_user_task_assignee(
            self, user_id: str, task_id: str,
            assigned_by: str) -> TaskAssigneeDTO | None:
        try:
            assignee_data = TaskAssignee.objects.get(
                user_id=user_id, task_id=task_id, assigned_by=assigned_by)

            return self._assignee_dto(assignee_data=assignee_data)
        except TaskAssignee.DoesNotExist:
            return None

    def reassign_task_assignee(self, assign_id: str) -> TaskAssigneeDTO:
        assignee_data = TaskAssignee.objects.get(assign_id=assign_id)
        assignee_data.is_active = True
        assignee_data.save()

        return self._assignee_dto(assignee_data=assignee_data)

    def get_assignees_for_list_tasks(self, list_id: str) -> list[
        TaskAssigneeDTO]:
        task_ids = (Task.objects.filter(list_id=list_id, is_deleted=False).
                    values_list('task_id', flat=True))
        task_assignees = TaskAssignee.objects.filter(task_id__in=task_ids,
                                                     is_active=True)

        return [self._assignee_dto(assignee_data=data) for data in
                task_assignees]
