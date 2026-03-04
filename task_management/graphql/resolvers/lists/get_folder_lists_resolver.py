from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import (
    FolderNotFoundType,
    DeletedFolderType,
)
from task_management.graphql.types.types import ListType, ListsType
from task_management.interactors.lists.get_folder_lists_interactor import (
    GetFolderListsInteractor,
)
from task_management.storages import ListStorage, FolderStorage


def get_folder_lists_resolver(root, info, params):
    folder_id = params.folder_id
    list_storage = ListStorage()
    folder_storage = FolderStorage()

    interactor = GetFolderListsInteractor(
        list_storage=list_storage,
        folder_storage=folder_storage,
    )

    try:
        lists_data = interactor.get_folder_lists(folder_id=folder_id)

        result = [
            ListType(
                list_id=list_item.list_id,
                name=list_item.name,
                description=list_item.description,
                entity_type=list_item.entity_type.value,
                entity_id=list_item.entity_id,
                is_deleted=list_item.is_deleted,
                order=list_item.order,
                is_private=list_item.is_private,
                created_by=list_item.created_by,
            )
            for list_item in lists_data
        ]

        return ListsType(lists=result)

    except custom_exceptions.FolderNotFound as e:
        return FolderNotFoundType(folder_id=e.folder_id)

    except custom_exceptions.DeletedFolderException as e:
        return DeletedFolderType(folder_id=e.folder_id)
