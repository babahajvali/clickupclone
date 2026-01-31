import graphene
from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import UserNotFoundType, \
    InactiveUserType, \
    AccountNotFoundType, InactiveAccountType, ModificationNotAllowedType
from task_management.graphql.types.input_types import \
    CreateWorkspaceInputParams
from task_management.graphql.types.response_types import \
    CreateWorkspaceResponse

from task_management.graphql.types.types import WorkspaceType

from task_management.interactors.dtos import CreateWorkspaceDTO
from task_management.interactors.workspace_interactors.workspace_interactors import \
    WorkspaceInteractor
from task_management.storages.workspace_member import WorkspaceMemberStorage
from task_management.storages.workspace_storage import WorkspaceStorage
from task_management.storages.user_storage import UserStorage
from task_management.storages.account_storage import AccountStorage
from task_management.storages.account_member_storage import \
    AccountMemberStorage


class CreateWorkspaceMutation(graphene.Mutation):
    class Arguments:
        params = CreateWorkspaceInputParams(required=True)

    Output = CreateWorkspaceResponse

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
            create_workspace_data = CreateWorkspaceDTO(
                name=params.name,
                description=params.description,
                user_id=info.context.user_id,
                account_id=params.account_id
            )

            result = interactor.create_workspace(
                create_workspace_data=create_workspace_data
            )

            return WorkspaceType(
                workspace_id=result.workspace_id,
                name=result.name,
                description=result.description,
                user_id=result.user_id,
                account_id=result.account_id,
                is_active=result.is_active
            )

        except custom_exceptions.UserNotFoundException as e:
            return UserNotFoundType(user_id=e.user_id)

        except custom_exceptions.InactiveUserException as e:
            return InactiveUserType(user_id=e.user_id)

        except custom_exceptions.AccountNotFoundException as e:
            return AccountNotFoundType(account_id=e.account_id)

        except custom_exceptions.InactiveAccountException as e:
            return InactiveAccountType(account_id=e.account_id)

        except custom_exceptions.ModificationNotAllowedException as e:
            return ModificationNotAllowedType(user_id=e.user_id)
