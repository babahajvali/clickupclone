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
from task_management.interactors.workspace.workspace_handler import \
    WorkspaceHandler
from task_management.storages.field_storage import FieldStorage
from task_management.storages.folder_storage import FolderStorage

from task_management.storages.list_storage import ListStorage
from task_management.storages.space_storage import SpaceStorage
from task_management.storages.template_storage import TemplateStorage
from task_management.storages.view_storage import ViewStorage
from task_management.storages.workspace_storage import WorkspaceStorage
from task_management.storages.user_storage import UserStorage
from task_management.storages.account_storage import AccountStorage



class CreateWorkspaceMutation(graphene.Mutation):
    class Arguments:
        params = CreateWorkspaceInputParams(required=True)

    Output = CreateWorkspaceResponse

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
            create_workspace_data = CreateWorkspaceDTO(
                name=params.name,
                description=params.description,
                user_id=info.context.user_id,
                account_id=params.account_id
            )

            result = workspace_onboarding.handle(
                workspace_data=create_workspace_data
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
