from datetime import date

from task_management.interactors.dtos import TaskAssigneeDTO, \
    TaskAssigneeDTO, UserTasksDTO, TaskDTO
from task_management.interactors.storage_interface.task_assignee_storage_interface import \
    TaskAssigneeStorageInterface
from task_management.models import User, Task, TaskAssignee


class TaskAssigneeStorage(TaskAssigneeStorageInterface):

    @staticmethod
    def _assignee_dto(assignee_data: TaskAssignee) -> TaskAssigneeDTO:
        return TaskAssigneeDTO(
            assign_id=assignee_data.assign_id,
            task_id=assignee_data.task.task_id,
            user_id=assignee_data.user.user_id,
            is_active=assignee_data.is_active,
            assigned_by=assignee_data.assigned_by.user_id,
        )

    def assign_task_assignee(self, task_id: str, user_id: str,
                             assigned_by: str) -> TaskAssigneeDTO:
        user = User.objects.get(user_id=user_id)
        task = Task.objects.get(task_id=task_id)
        assigned_by = User.objects.get(user_id=assigned_by)

        assignment_obj = TaskAssignee.objects.create(
            assigned_by=assigned_by,
            task=task, user=user
        )
        
        # Refresh with related objects for DTO conversion
        assignment_obj = TaskAssignee.objects.select_related(
            'task', 'user', 'assigned_by'
        ).get(assign_id=assignment_obj.assign_id)

        return self._assignee_dto(assignee_data=assignment_obj)

    def remove_task_assignee(self, assign_id: str) -> TaskAssigneeDTO:
        assignee_data = TaskAssignee.objects.select_related(
            'task', 'user', 'assigned_by'
        ).get(assign_id=assign_id)
        assignee_data.is_active = False
        assignee_data.save()

        return self._assignee_dto(assignee_data=assignee_data)

    def get_task_assignee(self, assign_id: str) -> TaskAssigneeDTO:
        assignee_data = TaskAssignee.objects.select_related(
            'task', 'user', 'assigned_by'
        ).get(assign_id=assign_id)

        return self._assignee_dto(assignee_data=assignee_data)

    def get_task_assignees(self, task_id: str) -> list[TaskAssigneeDTO]:
        task_assignees = TaskAssignee.objects.filter(
            task_id=task_id
        ).select_related('task', 'user', 'assigned_by')

        return [self._assignee_dto(assignee_data=data) for data in
                task_assignees]

    def get_user_assigned_tasks(self, user_id: str) -> UserTasksDTO:
        assignees = TaskAssignee.objects.filter(
            user_id=user_id, is_active=True, task__is_deleted=False
        ).select_related(
            'task__list', 'task__created_by', 'task'
        )

        tasks = []
        for assignee in assignees:
            tasks.append(TaskDTO(
                task_id=str(assignee.task.task_id),
                title=assignee.task.title,
                description=assignee.task.description,
                list_id=str(assignee.task.list.list_id),
                order=assignee.task.order,
                created_by=str(assignee.task.created_by.user_id),
                is_deleted=assignee.task.is_deleted
            ))

        return UserTasksDTO(
            user_id=user_id,
            tasks=tasks
        )

    def get_user_today_tasks(self, user_id: str) -> UserTasksDTO:
        today = date.today()

        assignees = TaskAssignee.objects.filter(
            user_id=user_id,
            is_active=True,
            task__is_deleted=False,
            assigned_at__date=today
        ).select_related(
            'task__list', 'task__created_by', 'task'
        )

        tasks = []
        for assignee in assignees:
            tasks.append(TaskDTO(
                task_id=str(assignee.task.task_id),
                title=assignee.task.title,
                description=assignee.task.description,
                list_id=str(assignee.task.list.list_id),
                order=assignee.task.order,
                created_by=str(assignee.task.created_by.user_id),
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
            assignee_data = TaskAssignee.objects.select_related(
                'task', 'user', 'assigned_by'
            ).get(
                user_id=user_id, task_id=task_id, assigned_by=assigned_by
            )

            return self._assignee_dto(assignee_data=assignee_data)
        except TaskAssignee.DoesNotExist:
            return None

    def reassign_task_assignee(self, assign_id: str) -> TaskAssigneeDTO:
        assignee_data = TaskAssignee.objects.select_related(
            'task', 'user', 'assigned_by'
        ).get(assign_id=assign_id)
        assignee_data.is_active = True
        assignee_data.save()

        return self._assignee_dto(assignee_data=assignee_data)
