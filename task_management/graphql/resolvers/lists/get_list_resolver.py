from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import ListNotFoundType
from task_management.graphql.types.types import ListType
from task_management.interactors.lists.get_list_interactor import (
    GetListInteractor,
)
from task_management.storages import ListStorage


def get_list_resolver(root, info, params):
    list_storage = ListStorage()

    interactor = GetListInteractor(
        list_storage=list_storage,
    )

    try:
        list_data = interactor.get_list(list_id=params.list_id)

        list_output = ListType(
            list_id=list_data.list_id,
            name=list_data.name,
            description=list_data.description,
            entity_type=list_data.entity_type.value,
            entity_id=list_data.entity_id,
            is_deleted=list_data.is_deleted,
            order=list_data.order,
            is_private=list_data.is_private,
            created_by=list_data.created_by,
        )

        return list_output

    except custom_exceptions.ListNotFound as e:
        return ListNotFoundType(list_id=e.list_id)
