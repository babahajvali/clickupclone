import graphene

from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import \
    AccountNameAlreadyExistsType, UserNotFoundType, InactiveUserType, \
    EmptyAccountNameExistsType
from task_management.graphql.types.input_types import CreateAccountInputParams
from task_management.graphql.types.response_types import CreateAccountResponse
from task_management.graphql.types.types import AccountType
from task_management.interactors.accounts.account_onboarding import \
    AccountOnboardingHandler
from task_management.storages import UserStorage, AccountStorage, \
    WorkspaceStorage, SpaceStorage, ListStorage, TemplateStorage, FieldStorage, \
    FolderStorage, ViewStorage


class CreateAccountMutation(graphene.Mutation):
    class Arguments:
        params = CreateAccountInputParams(required=True)

    Output = CreateAccountResponse

    @staticmethod
    def mutate(root, info, params):
        name = params.name
        description = params.description
        owner_id = params.owner_id

        user_storage = UserStorage()
        account_storage = AccountStorage()
        workspace_storage = WorkspaceStorage()
        space_storage = SpaceStorage()
        list_storage = ListStorage()
        template_storage = TemplateStorage()
        field_storage = FieldStorage()
        folder_storage = FolderStorage()
        view_storage = ViewStorage()

        account_onboarding = AccountOnboardingHandler(
            user_storage=user_storage,
            account_storage=account_storage,
            workspace_storage=workspace_storage,
            space_storage=space_storage,
            list_storage=list_storage,
            template_storage=template_storage,
            field_storage=field_storage,
            folder_storage=folder_storage,
            view_storage=view_storage, )

        try:
            result = account_onboarding.handle_account_onboarding(
                name=name, description=description, created_by=owner_id)

            return AccountType(
                account_id=result.account_id,
                name=result.name,
                description=result.description,
                owner_id=result.owner_id,
                is_active=result.is_active,
            )
        except custom_exceptions.AccountNameAlreadyExists as e:
            return AccountNameAlreadyExistsType(name=e.name)
        except custom_exceptions.UserNotFound as e:
            return UserNotFoundType(user_id=e.user_id)
        except custom_exceptions.InactiveUser as e:
            return InactiveUserType(user_id=e.user_id)
        except custom_exceptions.EmptyName as e:
            return EmptyAccountNameExistsType(name=e.name)
