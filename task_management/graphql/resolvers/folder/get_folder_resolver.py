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
        folder_dto = interactor.get_folder(folder_id=folder_id)

        folder_output = FolderType(
            folder_id=folder_dto.folder_id,
            name=folder_dto.name,
            description=folder_dto.description,
            space_id=folder_dto.space_id,
            order=folder_dto.order,
            is_deleted=folder_dto.is_deleted,
            created_by=folder_dto.created_by,
            is_private=folder_dto.is_private
        )

        return folder_output

    except custom_exceptions.FolderNotFound as e:
        return FolderNotFoundType(folder_id=e.folder_id)
