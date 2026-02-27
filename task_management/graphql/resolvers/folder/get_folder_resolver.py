from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import FolderNotFoundType
from task_management.graphql.types.types import FolderType
from task_management.interactors.folders.get_folder_interactor import \
    GetFolderInteractor
from task_management.storages import FolderStorage


def get_folder_resolver(root, info, params):
    folder_id = params.folder_id

    folder_storage = FolderStorage()

    interactor = GetFolderInteractor(
        folder_storage=folder_storage,
    )

    try:
        folder_data = interactor.get_folder(folder_id=folder_id)

        folder_output = FolderType(
            folder_id=folder_data.folder_id,
            name=folder_data.name,
            description=folder_data.description,
            space_id=folder_data.space_id,
            order=folder_data.order,
            is_active=folder_data.is_deleted,
            created_by=folder_data.created_by,
            is_private=folder_data.is_private
        )

        return folder_output

    except custom_exceptions.FolderNotFound as e:
        return FolderNotFoundType(folder_id=e.folder_id)
