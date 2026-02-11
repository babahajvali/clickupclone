from task_management.interactors.dtos import CreateWorkspaceDTO, \
    CreateSpaceDTO, CreateListDTO
from task_management.interactors.list_interactors.list_interactors import \
    ListInteractor
from task_management.interactors.space_interactors.space_interactors import \
    SpaceInteractor
from task_management.interactors.workspace_interactors.workspace_interactors import \
    WorkspaceInteractor
from task_management.interactors.workspace_interactors.workspace_transfer_service import \
    WorkspaceOnboardingHandler
from task_management.signal_services.default_space_list_creation_service import \
    DefaultSpaceListCreationService
from task_management.storages.account_storage import AccountStorage
from task_management.storages.field_storage import FieldStorage
from task_management.storages.folder_permission_storage import \
    FolderPermissionStorage
from task_management.storages.folder_storage import FolderStorage
from task_management.storages.list_permission_storage import \
    ListPermissionStorage
from task_management.storages.list_storage import ListStorage
from task_management.storages.space_permission_storage import \
    SpacePermissionStorage
from task_management.storages.space_storage import SpaceStorage
from task_management.storages.template_storage import TemplateStorage
from task_management.storages.user_storage import UserStorage
from task_management.storages.workspace_member import WorkspaceMemberStorage
from task_management.storages.workspace_storage import WorkspaceStorage


class CreateDefaultWorkspaceService:

    @staticmethod
    def create_default_workspace(workspace_input: CreateWorkspaceDTO):
        workspace_storage = WorkspaceStorage()
        user_storage = UserStorage()
        workspace_member_storage = WorkspaceMemberStorage()
        account_storage = AccountStorage()

        workspace_interactor = WorkspaceInteractor(
            workspace_storage=workspace_storage,
            user_storage=user_storage,
            workspace_member_storage=workspace_member_storage,
            account_storage=account_storage,
        )

        return workspace_interactor.create_workspace(workspace_input)
