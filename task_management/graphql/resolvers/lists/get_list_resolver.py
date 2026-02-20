from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import ListNotFoundType, \
    InactiveListType
from task_management.graphql.types.types import ListType
from task_management.interactors.list.list_interactor import \
    ListInteractor
from task_management.storages import ListStorage, FolderStorage, SpaceStorage, \
    WorkspaceStorage


def get_list_resolver(root, info, params):
    list_storage = ListStorage()
    folder_storage = FolderStorage()
    space_storage = SpaceStorage()
    workspace_storage = WorkspaceStorage()

    interactor = ListInteractor(
        list_storage=list_storage,
        folder_storage=folder_storage,
        space_storage=space_storage,
        workspace_storage=workspace_storage
    )

    try:
        list_data = interactor.get_active_list(list_id=params.list_id)

        list_output = ListType(
            list_id=list_data.list_id,
            name=list_data.name,
            description=list_data.description,
            space_id=list_data.space_id,
            is_active=list_data.is_active,
            order=list_data.order,
            is_private=list_data.is_private,
            created_by=list_data.created_by,
            folder_id=list_data.folder_id if list_data.folder_id else None
        )

        return list_output

    except custom_exceptions.ListNotFound as e:
        return ListNotFoundType(list_id=e.list_id)
    except custom_exceptions.InactiveList as e:
        return InactiveListType(list_id=e.list_id)
