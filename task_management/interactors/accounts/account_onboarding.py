from typing import Optional

from django.db import transaction

from task_management.interactors.accounts.account import Account
from task_management.interactors.dtos import CreateWorkspaceDTO
from task_management.interactors.storage_interfaces import \
    WorkspaceStorageInterface, UserStorageInterface, AccountStorageInterface, \
    SpaceStorageInterface, ListStorageInterface, \
    TemplateStorageInterface, FieldStorageInterface, FolderStorageInterface

from task_management.interactors.workspace.workspace import \
    Workspace


class AccountOnboardingHandler:
    """
    This Handler handle the create the account along with
        default workspace and space, list...

    """

    def __init__(self, workspace_storage: WorkspaceStorageInterface,
                 user_storage: UserStorageInterface,
                 account_storage: AccountStorageInterface,
                 space_storage: SpaceStorageInterface,
                 list_storage: ListStorageInterface,
                 template_storage: TemplateStorageInterface,
                 field_storage: FieldStorageInterface,
                 folder_storage: FolderStorageInterface):
        self.workspace_storage = workspace_storage
        self.user_storage = user_storage
        self.account_storage = account_storage
        self.space_storage = space_storage
        self.list_storage = list_storage
        self.template_storage = template_storage
        self.field_storage = field_storage
        self.folder_storage = folder_storage

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
            space_storage=self.space_storage,
            list_storage=self.list_storage,
            folder_storage=self.folder_storage,
            template_storage=self.template_storage,
            field_storage=self.field_storage,
            account_storage=self.account_storage,
        )
        workspace_interactor = Workspace(
            workspace_storage=self.workspace_storage,
            account_storage=self.account_storage,
            user_storage=self.user_storage
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
