from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import UserNotFoundType, \
    InactiveUserType
from task_management.graphql.types.types import AccountMemberType, \
    AccountMembersType
from task_management.interactors.account_interactor.account_member_interactor import \
    AccountMemberInteractor
from task_management.storages.account_member_storage import \
    AccountMemberStorage
from task_management.storages.account_storage import AccountStorage
from task_management.storages.folder_permission_storage import \
    FolderPermissionStorage
from task_management.storages.folder_storage import FolderStorage
from task_management.storages.list_permission_storage import \
    ListPermissionStorage
from task_management.storages.list_storage import ListStorage
from task_management.storages.space_permission_storage import \
    SpacePermissionStorage
from task_management.storages.space_storage import SpaceStorage
from task_management.storages.user_storage import UserStorage
from task_management.storages.workspace_member import WorkspaceMemberStorage
from task_management.storages.workspace_storage import WorkspaceStorage


def get_user_account_resolver(root,info):
    account_member_storage = AccountMemberStorage()
    account_storage = AccountStorage()
    user_storage = UserStorage()
    workspace_storage = WorkspaceStorage()
    workspace_member_storage = WorkspaceMemberStorage()
    space_permission_storage = SpacePermissionStorage()
    folder_permission_storage = FolderPermissionStorage()
    list_permission_storage = ListPermissionStorage()
    space_storage = SpaceStorage()
    folder_storage = FolderStorage()
    list_storage = ListStorage()

    interactor = AccountMemberInteractor(
        account_member_storage=account_member_storage,
        account_storage=account_storage,
        user_storage=user_storage,
        workspace_storage=workspace_storage,
        workspace_member_storage=workspace_member_storage,
        space_permission_storage=space_permission_storage,
        folder_permission_storage=folder_permission_storage,
        list_permission_storage=list_permission_storage,
        space_storage=space_storage,
        folder_storage=folder_storage,
        list_storage=list_storage
    )

    try:
        user_id = info.context.user_id

        accounts_data = interactor.get_user_accounts(user_id=user_id)
        results = [ AccountMemberType(
            id=result.id,
            account_id=result.account_id,
            user_id=result.user_id,
            role=result.role,
            is_active=result.is_active,
            added_by=result.added_by
        ) for result in accounts_data]


        return AccountMembersType(accounts=results)

    except custom_exceptions.UserNotFoundException as e:
        return UserNotFoundType(user_id=e.user_id)

    except custom_exceptions.InactiveUserException as e:
        return InactiveUserType(user_id=e.user_id)