from task_management.interactors.dtos import CreateWorkspaceDTO

from task_management.interactors.storage_interface.account_storage_interface import \
    AccountStorageInterface
from task_management.interactors.storage_interface.field_storage_interface import \
    FieldStorageInterface
from task_management.interactors.storage_interface.folder_permission_storage_interface import \
    FolderPermissionStorageInterface
from task_management.interactors.storage_interface.folder_storage_interface import \
    FolderStorageInterface
from task_management.interactors.storage_interface.list_permission_storage_interface import \
    ListPermissionStorageInterface
from task_management.interactors.storage_interface.list_storage_interface import \
    ListStorageInterface
from task_management.interactors.storage_interface.space_permission_storage_interface import \
    SpacePermissionStorageInterface
from task_management.interactors.storage_interface.space_storage_interface import \
    SpaceStorageInterface
from task_management.interactors.storage_interface.template_storage_interface import \
    TemplateStorageInterface
from task_management.interactors.storage_interface.user_storage_interface import \
    UserStorageInterface
from task_management.interactors.storage_interface.workspace_member_storage_interface import \
    WorkspaceMemberStorageInterface
from task_management.interactors.storage_interface.workspace_storage_interface import \
    WorkspaceStorageInterface
from task_management.interactors.workspace_interactors.workspace_interactors import \
    WorkspaceInteractor
from task_management.interactors.workspace_interactors.workspace_onboarding import \
    WorkspaceOnboardingHandler


class AccountOnboardingHandler:
    def __init__(self, workspace_storage: WorkspaceStorageInterface,
                 user_storage: UserStorageInterface,
                 account_storage: AccountStorageInterface,
                 workspace_member_storage: WorkspaceMemberStorageInterface,
                 space_storage: SpaceStorageInterface,
                 space_permission_storage: SpacePermissionStorageInterface,
                 list_storage: ListStorageInterface,
                 list_permission_storage: ListPermissionStorageInterface,
                 template_storage: TemplateStorageInterface,
                 field_storage: FieldStorageInterface,
                 folder_storage: FolderStorageInterface,
                 folder_permission_storage: FolderPermissionStorageInterface):
        self.workspace_storage = workspace_storage
        self.user_storage = user_storage
        self.account_storage = account_storage
        self.workspace_member_storage = workspace_member_storage
        self.space_storage = space_storage
        self.space_permission_storage = space_permission_storage
        self.list_storage = list_storage
        self.list_permission_storage = list_permission_storage
        self.template_storage = template_storage
        self.field_storage = field_storage
        self.folder_storage = folder_storage
        self.folder_permission_storage = folder_permission_storage

    def create_default_workspace(self, owner_id: str, account_id: str,
                                 name: str):
        workspace_onboarding = WorkspaceOnboardingHandler(
            workspace_storage=self.workspace_storage,
            user_storage=self.user_storage,
            workspace_member_storage=self.workspace_member_storage,
            space_storage=self.space_storage,
            space_permission_storage=self.space_permission_storage,
            list_storage=self.list_storage,
            list_permission_storage=self.list_permission_storage,
            folder_storage=self.folder_storage,
            folder_permission_storage=self.folder_permission_storage,
            template_storage=self.template_storage,
            field_storage=self.field_storage,
        )
        workspace_interactor = WorkspaceInteractor(
            workspace_storage=self.workspace_storage,
            user_storage=self.user_storage,
            account_storage=self.account_storage,
            workspace_member_storage=self.workspace_member_storage,
            workspace_onboarding=workspace_onboarding,
        )

        workspace_input_data = CreateWorkspaceDTO(
            name=f"{name}'s Workspace",
            description=f"Default workspace",
            user_id=owner_id,
            account_id=account_id
        )
        return workspace_interactor.create_workspace(workspace_input_data)
