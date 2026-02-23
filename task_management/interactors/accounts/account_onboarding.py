from typing import Optional

from django.db import transaction

from task_management.interactors.accounts.account_interactor import \
    AccountInteractor
from task_management.interactors.dtos import AccountDTO
from task_management.interactors.storage_interfaces import \
    WorkspaceStorageInterface, UserStorageInterface, AccountStorageInterface, \
    SpaceStorageInterface, ListStorageInterface, \
    TemplateStorageInterface, FieldStorageInterface, FolderStorageInterface, \
    ViewStorageInterface


class AccountOnboardingHandler:
    """
    This Handler handle the create the accounts along with
        default workspaces and spaces, lists...

    """

    def __init__(self, workspace_storage: WorkspaceStorageInterface,
                 user_storage: UserStorageInterface,
                 account_storage: AccountStorageInterface,
                 space_storage: SpaceStorageInterface,
                 list_storage: ListStorageInterface,
                 template_storage: TemplateStorageInterface,
                 field_storage: FieldStorageInterface,
                 folder_storage: FolderStorageInterface,
                 view_storage: ViewStorageInterface):
        self.workspace_storage = workspace_storage
        self.user_storage = user_storage
        self.account_storage = account_storage
        self.space_storage = space_storage
        self.list_storage = list_storage
        self.template_storage = template_storage
        self.field_storage = field_storage
        self.folder_storage = folder_storage
        self.view_storage = view_storage

    @transaction.atomic
    def handle_account_onboarding(
            self, name: str, created_by: str, description: Optional[str]) \
            -> AccountDTO:
        account_data = self._create_account(
            name=name, created_by=created_by, description=description)

        self._create_default_workspace(
            account_id=account_data.account_id, owner_id=created_by, name=name)

        return account_data

    def _create_account(self, name: str, created_by: str,
                        description: Optional[str]):
        """ First create the accounts interactor
        and the create accounts based on input data"""
        account_interactor = AccountInteractor(
            account_storage=self.account_storage,
            user_storage=self.user_storage,
        )
        return account_interactor.create_account(
            name=name, created_by=created_by, description=description)

    def _create_default_workspace(self, owner_id: str, account_id: str,
                                  name: str):
        """ Create default workspaces
        create the workspaces interactor
        then create the workspaces"""

        from task_management.interactors.workspaces.workspace_handler import \
            WorkspaceHandler
        workspace_onboarding = WorkspaceHandler(
            workspace_storage=self.workspace_storage,
            user_storage=self.user_storage,
            space_storage=self.space_storage,
            list_storage=self.list_storage,
            folder_storage=self.folder_storage,
            template_storage=self.template_storage,
            field_storage=self.field_storage,
            account_storage=self.account_storage,
            view_storage=self.view_storage
        )

        return workspace_onboarding.handle_workspace(
            account_id=account_id, user_id=owner_id, name=name,
            description=None)
