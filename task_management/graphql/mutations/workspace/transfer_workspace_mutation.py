import graphene

from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import WorkspaceNotFoundType, \
    UserNotWorkspaceOwnerType, UserNotFoundType, InactiveUserType
from task_management.graphql.types.input_types import \
    TransferWorkspaceInputParams
from task_management.graphql.types.response_types import \
    TransferWorkspaceResponse
from task_management.graphql.types.types import WorkspaceType
from task_management.interactors.workspace.workspace_handler import \
    WorkspaceHandler
from task_management.storages import WorkspaceStorage, UserStorage, \
    AccountStorage, SpaceStorage, FolderStorage, ListStorage, ViewStorage, \
    TemplateStorage, FieldStorage


class TransferWorkspaceMutation(graphene.Mutation):
    class Arguments:
        params = TransferWorkspaceInputParams(required=True)

    Output = TransferWorkspaceResponse

    @staticmethod
    def mutate(root, info, params):
        workspace_storage = WorkspaceStorage()
        user_storage = UserStorage()
        account_storage = AccountStorage()
        space_storage = SpaceStorage()
        folder_storage = FolderStorage()
        list_storage = ListStorage()
        view_storage = ViewStorage()
        template_storage = TemplateStorage()
        field_storage = FieldStorage()

        workspace_onboarding = WorkspaceHandler(
            workspace_storage=workspace_storage,
            user_storage=user_storage,
            space_storage=space_storage,
            list_storage=list_storage,
            folder_storage=folder_storage,
            template_storage=template_storage,
            field_storage=field_storage,
            account_storage=account_storage,
            view_storage=view_storage
        )

        try:
            result = workspace_onboarding.transfer_the_workspace(
                workspace_id=params.workspace_id,
                current_user_id=info.context.user_id,
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
