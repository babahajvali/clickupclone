from task_management.interactors.dtos import CreateSpaceDTO, CreateListDTO
from task_management.interactors.list_interactors.list_interactors import \
    ListInteractor
from task_management.interactors.space_interactors.space_interactors import \
    SpaceInteractor
from task_management.storages.field_storage import FieldStorage

from task_management.storages.folder_storage import FolderStorage
from task_management.storages.list_permission_storage import \
    ListPermissionStorage
from task_management.storages.list_storage import ListStorage
from task_management.storages.space_permission_storage import \
    SpacePermissionStorage
from task_management.storages.space_storage import SpaceStorage
from task_management.storages.template_storage import TemplateStorage
from task_management.storages.workspace_member import WorkspaceMemberStorage
from task_management.storages.workspace_storage import WorkspaceStorage


class DefaultSpaceListCreationService:

    @staticmethod
    def create_default_space_list(workspace_id: str, user_id: str):
        workspace_storage = WorkspaceStorage()
        workspace_member_storage = WorkspaceMemberStorage()
        list_storage = ListStorage()
        list_permission_storage = ListPermissionStorage()
        folder_storage = FolderStorage()
        space_storage = SpaceStorage()
        space_permission_storage = SpacePermissionStorage()
        field_storage = FieldStorage()
        template_storage = TemplateStorage()

        space_interactor = SpaceInteractor(
            space_storage=space_storage,
            space_permission_storage=space_permission_storage,
            workspace_storage=workspace_storage,
            workspace_member_storage=workspace_member_storage,
        )

        space_input_data = CreateSpaceDTO(
            name=f"Space",
            description=f"Default space",
            created_by=user_id,
            workspace_id=workspace_id,
            is_private=False
        )

        space_data = space_interactor.create_space(
            create_space_data=space_input_data)

        list_interactor = ListInteractor(
            list_storage=list_storage,
            list_permission_storage=list_permission_storage,
            template_storage=template_storage,
            field_storage=field_storage,
            workspace_member_storage=workspace_member_storage,
            space_storage=space_storage,
            folder_storage=folder_storage,
        )
        list_input_data = CreateListDTO(
            name=f"List 1",
            description=f"Default list",
            created_by=space_data.created_by,
            space_id=space_data.space_id,
            is_private=False,
            folder_id=None
        )

        return list_interactor.create_list(create_list_data=list_input_data)