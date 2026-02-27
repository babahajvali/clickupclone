from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import SpaceNotFoundType, \
    DeletedSpaceType
from task_management.graphql.types.types import FolderType, SpaceFoldersType
from task_management.interactors.folders.get_space_folders_interactor import \
    GetSpaceFoldersInteractor
from task_management.storages import FolderStorage, SpaceStorage


def get_space_folders_resolver(root, info, params):
    space_id = params.space_id

    folder_storage = FolderStorage()
    space_storage = SpaceStorage()

    interactor = GetSpaceFoldersInteractor(
        folder_storage=folder_storage,
        space_storage=space_storage
    )

    try:
        folders_data = interactor.get_space_folders(space_id=space_id)

        folders_output = [
            FolderType(
                folder_id=folder.folder_id,
                name=folder.name,
                description=folder.description,
                space_id=folder.space_id,
                order=folder.order,
                is_active=folder.is_deleted,
                created_by=folder.created_by,
                is_private=folder.is_private
            ) for folder in folders_data
        ]

        return SpaceFoldersType(folders=folders_output)

    except custom_exceptions.SpaceNotFound as e:
        return SpaceNotFoundType(space_id=e.space_id)

    except custom_exceptions.DeletedSpaceFound as e:
        return DeletedSpaceType(space_id=e.space_id)
