from typing import Optional, List

from django.db.models import F

from task_management.exceptions.enums import ListEntityType
from task_management.interactors.dtos import CreateTaskDTO, TaskDTO, \
    FilterDTO, TaskAssigneeDTO, UserTasksDTO
from task_management.interactors.storage_interfaces.task_storage_interface import \
    TaskStorageInterface
from task_management.models import Task, TaskAssignee, Space, Folder


class TaskStorage(TaskStorageInterface):
    @staticmethod
    def _convert_task_to_dto(task_data: Task) -> TaskDTO:
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
    def _convert_task_assignee_to_dto(
            assignee_data: TaskAssignee) -> TaskAssigneeDTO:
        return TaskAssigneeDTO(
            assign_id=assignee_data.assign_id,
            task_id=assignee_data.task.task_id,
            user_id=assignee_data.user.user_id,
            is_active=assignee_data.is_active,
            assigned_by=assignee_data.assigned_by.user_id,
        )

    def create_task(self, task_data: CreateTaskDTO, order: int) -> TaskDTO:

        task_obj = Task.objects.create(
            title=task_data.title, description=task_data.description,
            list_id=task_data.list_id, created_by_id=task_data.created_by,
            order=order)

        return self._convert_task_to_dto(task_data=task_obj)

    def get_last_task_order_in_list(self, list_id: str) -> int:
        last_task = Task.objects.filter(
            list_id=list_id, is_deleted=False).order_by('-order').first()

        return last_task.order if last_task else 0

    def update_task(
            self, task_id: str, title: Optional[str],
            description: Optional[str]) -> TaskDTO:

        task_data = Task.objects.get(task_id=task_id)

        is_title_provided = title is not None
        if is_title_provided:
            task_data.title = title

        is_description_provided = description is not None
        if is_description_provided:
            task_data.description = description

        task_data.save()

        return self._convert_task_to_dto(task_data=task_data)

    def get_task(self, task_id: str) -> TaskDTO | None:
        task_data = Task.objects.filter(task_id=task_id).first()

        is_task_not_found = not task_data
        if is_task_not_found:
            return None

        return self._convert_task_to_dto(task_data=task_data)

    def get_workspace_id_from_task_id(self, task_id: str) -> str | None:

        list_data = Task.objects.select_related("list").values(
            "list__entity_type",
            "list__entity_id",
        ).filter(task_id=task_id).first()

        if list_data is None:
            return None

        entity_type = list_data["list__entity_type"]
        entity_id = list_data["list__entity_id"]

        if entity_type == ListEntityType.SPACE.value:
            return str(Space.objects.values_list(
                "workspace_id", flat=True
            ).get(space_id=entity_id))

        return str(Folder.objects.values_list(
            "space__workspace_id", flat=True
        ).get(folder_id=entity_id))

    def get_tasks_for_list(self, list_id: str) -> List[TaskDTO]:
        list_tasks = Task.objects.filter(list_id=list_id, is_deleted=False)

        return [self._convert_task_to_dto(task_data=task_data) for task_data in
                list_tasks]

    def delete_task(self, task_id: str) -> TaskDTO:
        task_data = Task.objects.get(task_id=task_id)
        task_data.is_deleted = True
        task_data.save()
        current_order = task_data.order
        Task.objects.filter(
            list_id=task_data.list.list_id, is_deleted=False,
            order__gt=current_order).update(order=F("order") - 1)

        return self._convert_task_to_dto(task_data=task_data)

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

    def reorder_task(
            self, list_id: str, new_order: int, task_id: str) -> TaskDTO:
        task_data = Task.objects.get(task_id=task_id)
        task_data.order = new_order
        task_data.save()

        return self._convert_task_to_dto(task_data=task_data)

    def shift_tasks_down(
            self, list_id: str, current_order: int, new_order: int):

        Task.objects.filter(
            list_id=list_id,
            is_deleted=False,
            order__gt=current_order,
            order__lte=new_order
        ).update(order=F("order") - 1)

    def shift_tasks_up(
            self, list_id: str, current_order: int, new_order: int):
        Task.objects.filter(
            list_id=list_id,
            is_deleted=False,
            order__gte=new_order,
            order__lt=current_order
        ).update(order=F("order") + 1)

    def add_task_assignee(
            self, task_id: str, user_id: str,
            assigned_by: str) -> TaskAssigneeDTO:

        assignment_data = TaskAssignee.objects.create(
            assigned_by_id=assigned_by, task_id=task_id, user_id=user_id)

        return self._convert_task_assignee_to_dto(
            assignee_data=assignment_data)

    def remove_task_assignee(self, assign_id: str) -> TaskAssigneeDTO:
        assignee_data = TaskAssignee.objects.get(assign_id=assign_id)
        assignee_data.is_active = False
        assignee_data.save(update_fields=["is_active"])

        return self._convert_task_assignee_to_dto(assignee_data=assignee_data)

    def get_task_assignee(self, assign_id: str) -> TaskAssigneeDTO:
        assignee_data = TaskAssignee.objects.filter(
            assign_id=assign_id).first()

        return self._convert_task_assignee_to_dto(assignee_data=assignee_data)

    def get_task_assignees(self, task_id: str) -> List[TaskAssigneeDTO]:
        task_assignees = TaskAssignee.objects.filter(
            task_id=task_id, is_active=True)

        return [self._convert_task_assignee_to_dto(assignee_data=data) for data
                in
                task_assignees]

    def get_user_assigned_tasks(self, user_id: str) -> UserTasksDTO:
        assignees = TaskAssignee.objects.filter(
            user_id=user_id, is_active=True, task__is_deleted=False
        ).select_related('task', 'task__list')

        tasks = []
        for assignee in assignees:
            tasks.append(TaskDTO(
                task_id=str(assignee.task.task_id),
                title=assignee.task.title,
                description=assignee.task.description,
                list_id=str(assignee.task.list.list_id),
                order=assignee.task.order,
                created_by=str(assignee.task.created_by),
                is_deleted=assignee.task.is_deleted
            ))

        return UserTasksDTO(
            user_id=user_id,
            tasks=tasks
        )

    def get_user_task_assignee(
            self, user_id: str, task_id: str,
            assigned_by: str) -> TaskAssigneeDTO | None:

        assignee_data = TaskAssignee.objects.filter(
            user_id=user_id, task_id=task_id, assigned_by=assigned_by).first()

        if not assignee_data:
            return None

        return self._convert_task_assignee_to_dto(assignee_data=assignee_data)

    def reassign_task_assignee(self, assign_id: str) -> TaskAssigneeDTO:
        assignee_data = TaskAssignee.objects.get(assign_id=assign_id)
        assignee_data.is_active = True
        assignee_data.save(update_fields=["is_active"])

        return self._convert_task_assignee_to_dto(assignee_data=assignee_data)

    def get_assignees_for_list_tasks(
            self, list_id: str) -> List[TaskAssigneeDTO]:

        task_ids = (Task.objects.filter(list_id=list_id, is_deleted=False).
                    values_list('task_id', flat=True))
        task_assignees = TaskAssignee.objects.filter(
            task_id__in=task_ids, is_active=True)

        return [self._convert_task_assignee_to_dto(assignee_data=data) for data
                in
                task_assignees]
