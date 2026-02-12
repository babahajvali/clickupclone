import graphene

from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import WorkspaceNotFoundType, \
    InactiveWorkspaceType, UserNotWorkspaceOwnerType
from task_management.graphql.types.input_types import \
    DeleteWorkspaceInputParams
from task_management.graphql.types.response_types import \
    DeleteWorkspaceResponse
from task_management.graphql.types.types import WorkspaceType
from task_management.interactors.workspace.workspace import \
    Workspace

from task_management.storages.account_storage import AccountStorage
from task_management.storages.user_storage import UserStorage
from task_management.storages.workspace_storage import WorkspaceStorage


class DeleteWorkspaceMutation(graphene.Mutation):
    class Arguments:
        params = DeleteWorkspaceInputParams(required=True)

    Output = DeleteWorkspaceResponse

    @staticmethod
    def mutate(root, info, params):
        workspace_storage = WorkspaceStorage()
        user_storage = UserStorage()
        account_storage = AccountStorage()

        interactor = Workspace(
            workspace_storage=workspace_storage,
            user_storage=user_storage,
            account_storage=account_storage,
        )

        try:
            result = interactor.delete_workspace(
                workspace_id=params.workspace_id,
                user_id=info.context.user_id
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

        except custom_exceptions.InactiveWorkspaceException as e:
            return InactiveWorkspaceType(workspace_id=e.workspace_id)

        except custom_exceptions.UserNotWorkspaceOwnerException as e:
            return UserNotWorkspaceOwnerType(user_id=e.user_id)
