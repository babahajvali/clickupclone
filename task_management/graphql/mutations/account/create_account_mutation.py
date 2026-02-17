import graphene

from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import \
    AccountNameAlreadyExistsType, UserNotFoundType, InactiveUserType, \
    EmptyAccountNameExistsType
from task_management.graphql.types.input_types import CreateAccountInputParams
from task_management.graphql.types.response_types import CreateAccountResponse
from task_management.graphql.types.types import AccountType
from task_management.interactors.account.account import \
    Account
from task_management.storages import UserStorage, AccountStorage


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


        interactor = Account(
            user_storage=user_storage,
            account_storage=account_storage)

        try:
            result = interactor.create_account(name=name, description=description,created_by=owner_id)

            return AccountType(
                account_id=result.account_id,
                name=result.name,
                description=result.description,
                owner_id=result.owner_id,
                is_active=result.is_active,
            )
        except custom_exceptions.AccountNameAlreadyExistsException as e:
            return AccountNameAlreadyExistsType(name=e.name)
        except custom_exceptions.UserNotFoundException as e:
            return UserNotFoundType(user_id=e.user_id)
        except custom_exceptions.InactiveUserException as e:
            return InactiveUserType(user_id=e.user_id)
        except custom_exceptions.EmptyNameException as e:
            return EmptyAccountNameExistsType(name=e.name)

