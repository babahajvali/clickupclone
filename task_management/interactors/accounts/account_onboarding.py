from typing import Optional

from django.db import transaction

from task_management.interactors.accounts.account import Account
from task_management.interactors.dtos import CreateWorkspaceDTO
from task_management.interactors.storage_interfaces import \
    WorkspaceStorageInterface, UserStorageInterface, AccountStorageInterface, \
    WorkspaceMemberStorageInterface, SpaceStorageInterface, \
    SpacePermissionStorageInterface, ListStorageInterface, \
    ListPermissionStorageInterface, TemplateStorageInterface, \
    FieldStorageInterface, FolderStorageInterface, \
    FolderPermissionStorageInterface

from task_management.interactors.workspace.workspace import \
    Workspace


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

    @transaction.atomic
    def handle(self, name: str, created_by: str, description: Optional[str]):
        account_data = self._create_account(name=name, created_by=created_by,
                                            description=description)

        return self._create_default_workspace(
            account_id=account_data.account_id, owner_id=created_by, name=name)

    def _create_account(self, name: str, created_by: str,
                        description: Optional[str]):
        """ First create the account interactor
        and the create account based on input data"""
        account_interactor = Account(
            account_storage=self.account_storage,
            user_storage=self.user_storage,
        )
        return account_interactor.create_account(
            name=name, created_by=created_by, description=description)

    def _create_default_workspace(self, owner_id: str, account_id: str,
                                  name: str):
        """ Create default workspace
        create the workspace interactor
        then create the workspace"""

        from task_management.interactors.workspace.workspace_onboarding import \
            WorkspaceOnboardingHandler
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
        workspace_interactor = Workspace(
            workspace_storage=self.workspace_storage,
            account_storage=self.account_storage,
            workspace_member_storage=self.workspace_member_storage,
        )

        workspace_input_data = CreateWorkspaceDTO(
            name=f"{name}'s Workspace",
            description=f"Default workspace",
            user_id=owner_id,
            account_id=account_id
        )
        workspace_data = workspace_interactor.create_workspace(
            workspace_input_data)

        return workspace_onboarding.handle(
            workspace_id=workspace_data.workspace_id,
            user_id=workspace_data.user_id)
