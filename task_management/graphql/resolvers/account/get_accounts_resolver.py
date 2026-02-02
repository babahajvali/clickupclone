from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import \
    InvalidAccountIdsFoundType
from task_management.graphql.types.types import AccountType, AccountsType
from task_management.interactors.account_interactor.account_interactors import \
    AccountInteractor
from task_management.storages.account_member_storage import \
    AccountMemberStorage
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
from task_management.storages.task_storage import TaskStorage
from task_management.storages.template_storage import TemplateStorage
from task_management.storages.user_storage import UserStorage
from task_management.storages.workspace_member import WorkspaceMemberStorage
from task_management.storages.workspace_storage import WorkspaceStorage


def get_accounts_resolver(root, info, params):
    user_storage = UserStorage()
    account_storage = AccountStorage()
    account_member_storage = AccountMemberStorage()
    workspace_storage = WorkspaceStorage()
    workspace_member_storage = WorkspaceMemberStorage()
    space_storage = SpaceStorage()
    space_permission_storage = SpacePermissionStorage()
    folder_permission_storage = FolderPermissionStorage()
    folder_storage = FolderStorage()
    list_storage = ListStorage()
    list_permission_storage = ListPermissionStorage()
    template_storage = TemplateStorage()
    field_storage = FieldStorage()
    task_storage = TaskStorage()

    interactor = AccountInteractor(
        user_storage=user_storage,
        account_member_storage=account_member_storage,
        account_storage=account_storage,
        workspace_storage=workspace_storage,
        workspace_member_storage=workspace_member_storage,
        space_storage=space_storage,
        space_permission_storage=space_permission_storage,
        folder_permission_storage=folder_permission_storage,
        folder_storage=folder_storage,
        list_storage=list_storage,
        list_permission_storage=list_permission_storage,
        template_storage=template_storage,
        field_storage=field_storage,
        task_storage=task_storage)

    try:
        account_ids = params.account_ids

        accounts_data = interactor.get_accounts(account_ids=account_ids)

        results = [AccountType(
            account_id=result.account_id,
            name=result.name,
            description=result.description,
            owner_id=result.owner_id,
            is_active=result.is_active,
        )for result in accounts_data]

        return AccountsType(accounts=results)

    except custom_exceptions.InvalidAccountIdsFoundException as e:
        return InvalidAccountIdsFoundType(account_ids=e.account_ids)

