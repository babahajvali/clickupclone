from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import SpaceNotFoundType, \
    InactiveSpaceType
from task_management.graphql.types.types import FolderType, SpaceFoldersType
from task_management.interactors.space_interactors.folders_interactor import \
    FolderInteractor
from task_management.storages.folder_storage import FolderStorage
from task_management.storages.folder_permission_storage import FolderPermissionStorage
from task_management.storages.space_permission_storage import SpacePermissionStorage
from task_management.storages.space_storage import SpaceStorage


def get_space_folders_resolver(root, info, params):
    space_id = params.space_id

    folder_storage = FolderStorage()
    folder_permission_storage = FolderPermissionStorage()
    space_permission_storage = SpacePermissionStorage()
    space_storage = SpaceStorage()

    interactor = FolderInteractor(
        folder_storage=folder_storage,
        folder_permission_storage=folder_permission_storage,
        space_permission_storage=space_permission_storage,
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
                is_active=folder.is_active,
                created_by=folder.created_by,
                is_private=folder.is_private
            ) for folder in folders_data
        ]

        return SpaceFoldersType(folders=folders_output)

    except custom_exceptions.SpaceNotFoundException as e:
        return SpaceNotFoundType(space_id=e.space_id)

    except custom_exceptions.InactiveSpaceException as e:
        return InactiveSpaceType(space_id=e.space_id)
