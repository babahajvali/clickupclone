from django.core.exceptions import ObjectDoesNotExist
from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import ListNotFoundType, \
    InactiveListType, ModificationNotAllowedType, InvalidOffsetNumberType, \
    InvalidLimitType
from task_management.graphql.types.types import TaskType, TasksType

from task_management.interactors.dtos import FilterDTO
from task_management.interactors.task_interactors.task_interactor import \
    TaskInteractor
from task_management.storages.field_value_storage import FieldValueStorage
from task_management.storages.task_storage import TaskStorage
from task_management.storages.list_storage import ListStorage
from task_management.storages.list_permission_storage import \
    ListPermissionStorage
from task_management.storages.field_storage import FieldStorage


def task_filter_resolver(root, info, params):
    task_storage = TaskStorage()
    list_storage = ListStorage()
    permission_storage = ListPermissionStorage()
    field_storage = FieldStorage()
    field_value_storage = FieldValueStorage()

    interactor = TaskInteractor(
        task_storage=task_storage,
        list_storage=list_storage,
        permission_storage=permission_storage,
        field_storage=field_storage,
        field_value_storage=field_value_storage
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
            task_filter_data=filter_data,
            user_id=info.context.user_id
        )

        tasks_output = [
            TaskType(
                task_id=task.task_id,
                title=task.title,
                description=task.description,
                list_id=task.list_id,
                order=task.order,
                created_by=task.created_by,
                is_delete=task.is_deleted
            ) for task in tasks_data
        ]

        return TasksType(tasks=tasks_output)

    except ObjectDoesNotExist:
        return ModificationNotAllowedType(user_id=params.user_id)

    except custom_exceptions.ListNotFoundException as e:
        return ListNotFoundType(list_id=e.list_id)

    except custom_exceptions.InactiveListException as e:
        return InactiveListType(list_id=e.list_id)

    except custom_exceptions.InvalidOffsetNumberException as e:
        return InvalidOffsetNumberType(offset=e.offset)

    except custom_exceptions.InvalidLimitException as e:
        return InvalidLimitType(limit=e.limit)
