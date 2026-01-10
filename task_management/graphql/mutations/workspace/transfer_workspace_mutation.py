import graphene

from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import WorkspaceNotFoundType, \
    UserNotWorkspaceOwnerType, UserNotFoundType, InactiveUserType
from task_management.graphql.types.input_types import \
    TransferWorkspaceInputParams
from task_management.graphql.types.response_types import \
    TransferWorkspaceResponse
from task_management.graphql.types.types import WorkspaceType
from task_management.interactors.workspace_interactors.workspace_interactors import \
    WorkspaceInteractor
from task_management.storages.account_member_storage import \
    AccountMemberStorage
from task_management.storages.account_storage import AccountStorage
from task_management.storages.user_storage import UserStorage
from task_management.storages.workspace_member import WorkspaceMemberStorage
from task_management.storages.workspace_storage import WorkspaceStorage


class TransferWorkspaceMutation(graphene.Mutation):
    class Arguments:
        params = TransferWorkspaceInputParams(required=True)

    Output = TransferWorkspaceResponse

    @staticmethod
    def mutate(root, info, params):
        workspace_storage = WorkspaceStorage()
        user_storage = UserStorage()
        account_storage = AccountStorage()
        account_member_storage = AccountMemberStorage()
        workspace_member_storage = WorkspaceMemberStorage()

        interactor = WorkspaceInteractor(
            workspace_storage=workspace_storage,
            user_storage=user_storage,
            account_storage=account_storage,
            account_member_storage=account_member_storage,
            workspace_member_storage=workspace_member_storage
        )

        try:
            result = interactor.transfer_workspace(
                workspace_id=params.workspace_id,
                user_id=params.user_id,
                new_user_id=params.new_user_id
            )

            return WorkspaceType(
                workspace_id=result.workspace_id,
                name=result.name,
                description=result.description,
                user_id=result.user_id,
                account_id=result.account_id,
                is_active=result.is_active
            )

        except custom_exceptions.WorkspaceNotFoundException as e:
            return WorkspaceNotFoundType(workspace_id=e.workspace_id)

        except custom_exceptions.UserNotWorkspaceOwnerException as e:
            return UserNotWorkspaceOwnerType(user_id=e.user_id)

        except custom_exceptions.UserNotFoundException as e:
            return UserNotFoundType(user_id=e.user_id)

        except custom_exceptions.InactiveUserException as e:
            return InactiveUserType(user_id=e.user_id)
