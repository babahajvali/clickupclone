from django.core.exceptions import ObjectDoesNotExist
from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import ListNotFoundType, \
    InactiveListType, ModificationNotAllowedType, InvalidOffset, \
    InvalidLimitType
from task_management.graphql.types.types import TaskType, TasksType

from task_management.interactors.dtos import FilterDTO
from task_management.interactors.task.task_interactor import \
    TaskInteractor
from task_management.storages import ListStorage, TaskStorage, WorkspaceStorage


def task_filter_resolver(root, info, params):
    list_storage = ListStorage()
    task_storage = TaskStorage()
    workspace_storage = WorkspaceStorage()

    interactor = TaskInteractor(
        list_storage=list_storage,
        task_storage=task_storage,
        workspace_storage=workspace_storage,
    )

    try:
        filter_data = FilterDTO(
            list_id=params.list_id,
            field_filters=params.field_filters if params.field_filters else None,
            assignees=params.assignees if params.assignees else None,
            offset=params.offset if params.offset else 1,
            limit=params.limit if params.limit else 10
        )

        tasks_data = interactor.task_filter(
            task_filter_data=filter_data)

        tasks_output = [
            TaskType(
                task_id=task.task_id,
                title=task.title,
                description=task.description,
                list_id=task.list_id,
                order=task.order,
                created_by=task.created_by_user_id,
                is_delete=task.is_deleted
            ) for task in tasks_data
        ]

        return TasksType(tasks=tasks_output)

    except ObjectDoesNotExist:
        return ModificationNotAllowedType(user_id=params.user_id)

    except custom_exceptions.ListNotFound as e:
        return ListNotFoundType(list_id=e.list_id)

    except custom_exceptions.InactiveList as e:
        return InactiveListType(list_id=e.list_id)

    except custom_exceptions.InvalidOffset as e:
        return InvalidOffset(offset=e.offset)

    except custom_exceptions.InvalidLimit as e:
        return InvalidLimitType(limit=e.limit)
