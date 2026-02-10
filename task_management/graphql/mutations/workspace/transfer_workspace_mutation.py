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
from task_management.interactors.workspace_interactors.workspace_onboarding import \
    WorkspaceOnboardingHandler
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
from task_management.storages.template_storage import TemplateStorage
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
        workspace_member_storage = WorkspaceMemberStorage()
        space_storage = SpaceStorage()
        space_permission_storage = SpacePermissionStorage()
        folder_storage = FolderStorage()
        folder_permission_storage = FolderPermissionStorage()
        list_storage = ListStorage()
        list_permission_storage = ListPermissionStorage()
        template_storage = TemplateStorage()
        field_storage = FieldStorage()

        workspace_onboarding = WorkspaceOnboardingHandler(
            workspace_storage=workspace_storage,
            user_storage=user_storage,
            workspace_member_storage=workspace_member_storage,
            space_storage=space_storage,
            space_permission_storage=space_permission_storage,
            list_storage=list_storage,
            list_permission_storage=list_permission_storage,
            folder_storage=folder_storage,
            folder_permission_storage=folder_permission_storage,
            template_storage=template_storage,
            field_storage=field_storage,
        )

        interactor = WorkspaceInteractor(
            workspace_storage=workspace_storage,
            user_storage=user_storage,
            account_storage=account_storage,
            workspace_member_storage=workspace_member_storage,
            workspace_onboarding=workspace_onboarding,
        )

        try:
            result = interactor.transfer_workspace(
                workspace_id=params.workspace_id,
                user_id=info.context.user_id,
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
