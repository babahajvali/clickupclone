from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import SpaceNotFoundType, \
    InactiveSpaceType
from task_management.graphql.types.types import ListType, ListsType
from task_management.interactors.list.list_interactor import \
    ListInteractor
from task_management.storages import ListStorage, FolderStorage, SpaceStorage, \
    WorkspaceStorage


def get_space_lists_resolver(root, info, params):
    space_id = params.space_id

    list_storage = ListStorage()
    folder_storage = FolderStorage()
    space_storage = SpaceStorage()
    workspace_storage = WorkspaceStorage()

    interactor = ListInteractor(
        list_storage=list_storage,
        folder_storage=folder_storage,
        space_storage=space_storage,
        workspace_storage=workspace_storage)

    try:
        lists_data = interactor.get_active_space_lists(space_id=space_id)

        lists_output = [
            ListType(
                list_id=list_item.list_id,
                name=list_item.name,
                description=list_item.description,
                space_id=list_item.space_id,
                is_active=list_item.is_active,
                order=list_item.order,
                is_private=list_item.is_private,
                created_by=list_item.created_by_user_id,
                folder_id=list_item.folder_id if list_item.folder_id else None
            ) for list_item in lists_data
        ]

        return ListsType(lists=lists_output)

    except custom_exceptions.SpaceNotFoundException as e:
        return SpaceNotFoundType(space_id=e.space_id)

    except custom_exceptions.InactiveSpaceException as e:
        return InactiveSpaceType(space_id=e.space_id)
