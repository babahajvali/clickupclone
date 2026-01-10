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
from task_management.interactors.workspace_interactors.workspace_interactors import \
    WorkspaceInteractor
from task_management.storages.account_member_storage import \
    AccountMemberStorage
from task_management.storages.account_storage import AccountStorage
from task_management.storages.user_storage import UserStorage
from task_management.storages.workspace_member import WorkspaceMemberStorage
from task_management.storages.workspace_storage import WorkspaceStorage


class UpdateWorkspaceMutation(graphene.Mutation):
    class Arguments:
        params = UpdateWorkspaceInputParams(required=True)

    Output = UpdateWorkspaceResponse

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
            update_workspace_data = UpdateWorkspaceDTO(
                workspace_id=params.workspace_id,
                name=params.name,
                description=params.description
            )

            result = interactor.update_workspace(
                update_workspace_data=update_workspace_data,
                user_id=params.user_id
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
