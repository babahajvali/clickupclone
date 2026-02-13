from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import ListNotFoundType, \
    InactiveListType
from task_management.graphql.types.types import TaskType, TasksType, \
    TaskAssigneeType, FieldValuesType
from task_management.interactors.task.task_interactor import TaskInteractor
from task_management.interactors.task.task_assignee_interactor import \
    TaskAssigneeInteractor
from task_management.storages.space_storage import SpaceStorage
from task_management.storages.task_storage import TaskStorage
from task_management.storages.list_storage import ListStorage
from task_management.storages.workspace_storage import WorkspaceStorage
from task_management.storages.user_storage import UserStorage
from task_management.storages.field_storage import FieldStorage


def get_list_tasks_resolver(root, info, params):
    list_id = params.list_id

    list_storage = ListStorage()
    task_storage = TaskStorage()
    space_storage = SpaceStorage()
    workspace_storage = WorkspaceStorage()
    user_storage = UserStorage()
    field_storage = FieldStorage()

    task_interactor = TaskInteractor(
        list_storage=list_storage,
        task_storage=task_storage,
        space_storage=space_storage,
        workspace_storage=workspace_storage,
    )

    assignee_interactor = TaskAssigneeInteractor(
        user_storage=user_storage,
        task_storage=task_storage,
        list_storage=list_storage,
        space_storage=space_storage,
        workspace_storage=workspace_storage
    )

    try:
        tasks_data = task_interactor.get_list_tasks(list_id=list_id)
        task_ids = [task.task_id for task in tasks_data]

        assignees_data = assignee_interactor.get_assignees_for_list_tasks(
            list_id=list_id
        )

        field_values_data = field_storage.get_field_values_by_task_ids(
            task_ids=task_ids
        )

        assignees_by_task = {}
        for assignee in assignees_data:
            if assignee.task_id not in assignees_by_task:
                assignees_by_task[assignee.task_id] = []
            assignees_by_task[assignee.task_id].append(
                TaskAssigneeType(
                    assign_id=assignee.assign_id,
                    user_id=assignee.user_id,
                    task_id=assignee.task_id,
                    is_active=assignee.is_active,
                    assigned_by=assignee.assigned_by
                )
            )

        field_values_by_task = {}
        for task_field_data in field_values_data:
            task_id_str = str(task_field_data.task_id)

            field_values_by_task[task_id_str] = [
                FieldValuesType(
                    field_id=str(v.field_id),
                    value=v.value
                )
                for v in task_field_data.values
            ]

        tasks_output = [
            TaskType(
                task_id=task.task_id,
                title=task.title,
                description=task.description,
                list_id=task.list_id,
                order=task.order,
                created_by=task.created_by,
                is_delete=task.is_deleted,
                assignees=assignees_by_task.get(task.task_id, []),
                field_values=field_values_by_task.get(str(task.task_id), [])
            )
            for task in tasks_data
        ]

        return TasksType(tasks=tasks_output)

    except custom_exceptions.ListNotFoundException as e:
        return ListNotFoundType(list_id=e.list_id)
    except custom_exceptions.InactiveListException as e:
        return InactiveListType(list_id=e.list_id)