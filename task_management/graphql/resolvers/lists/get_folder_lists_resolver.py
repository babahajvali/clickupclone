from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import FolderNotFoundType, \
    InactiveFolderType
from task_management.graphql.types.types import ListType, ListsType
from task_management.interactors.list.list_interactor import \
    ListInteractor
from task_management.storages import ListStorage, FolderStorage, SpaceStorage, \
    WorkspaceStorage


def get_folder_lists_resolver(root, info, params):
    folder_id = params.folder_id
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
        lists_data = interactor.get_folder_lists(folder_id=folder_id)

        result = [
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

        return ListsType(lists=result)

    except custom_exceptions.FolderNotFoundException as e:
        return FolderNotFoundType(folder_id=e.folder_id)

    except custom_exceptions.InactiveFolderException as e:
        return InactiveFolderType(folder_id=e.folder_id)
