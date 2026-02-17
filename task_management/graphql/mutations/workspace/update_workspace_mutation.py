import graphene

from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import WorkspaceNotFoundType, \
    InactiveWorkspaceType, ModificationNotAllowedType
from task_management.graphql.types.input_types import \
    UpdateWorkspaceInputParams
from task_management.graphql.types.response_types import \
    UpdateWorkspaceResponse
from task_management.graphql.types.types import WorkspaceType
from task_management.interactors.dtos import UpdateWorkspaceDTO
from task_management.interactors.workspace.workspace import \
    Workspace
from task_management.storages import WorkspaceStorage, UserStorage, \
    AccountStorage


class UpdateWorkspaceMutation(graphene.Mutation):
    class Arguments:
        params = UpdateWorkspaceInputParams(required=True)

    Output = UpdateWorkspaceResponse

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
            update_workspace_data = UpdateWorkspaceDTO(
                workspace_id=params.workspace_id,
                name=params.name,
                description=params.description
            )

            result = interactor.update_workspace(
                workspace_data=update_workspace_data,
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


        except custom_exceptions.ModificationNotAllowedException as e:
            return ModificationNotAllowedType(user_id=e.user_id)
