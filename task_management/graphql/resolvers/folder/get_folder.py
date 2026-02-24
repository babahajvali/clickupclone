from django.core.exceptions import ObjectDoesNotExist
from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import FolderNotFoundType
from task_management.graphql.types.types import FolderType
from task_management.interactors.spaces.folder_interactor import \
    FolderInteractor
from task_management.storages import FolderStorage, SpaceStorage, \
    WorkspaceStorage


def get_folder_resolver(root, info, params):
    folder_id = params.folder_id

    folder_storage = FolderStorage()
    space_storage = SpaceStorage()
    workspace_storage = WorkspaceStorage()

    interactor = FolderInteractor(
        folder_storage=folder_storage,
        space_storage=space_storage,
        workspace_storage=workspace_storage
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
