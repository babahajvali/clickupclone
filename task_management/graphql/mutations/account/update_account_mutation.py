import graphene

from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import \
    AccountNameAlreadyExistsType, AccountNotFoundType, InactiveAccountType, \
    UserNotAccountOwnerType, NothingToUpdateAccountType
from task_management.graphql.types.input_types import UpdateAccountInputParams
from task_management.graphql.types.response_types import UpdateAccountResponse
from task_management.graphql.types.types import AccountType
from task_management.interactors.account.account_interactor import \
    AccountInteractor
from task_management.storages import UserStorage, AccountStorage


class UpdateAccountMutation(graphene.Mutation):
    class Arguments:
        params = UpdateAccountInputParams(required=True)

    Output = UpdateAccountResponse

    @staticmethod
    def mutate(root, info, params):
        user_id = info.context.user_id

        user_storage = UserStorage()
        account_storage = AccountStorage()

        interactor = AccountInteractor(
            user_storage=user_storage,
            account_storage=account_storage)

        try:

            result = interactor.update_account(
                account_id=params.account_id, name=params.name,
                description=params.description, user_id=user_id)

            return AccountType(
                account_id=result.account_id,
                name=result.name,
                description=result.description,
                owner_id=result.owner_id,
                is_active=result.is_active,
            )

        except custom_exceptions.AccountNameAlreadyExistsException as e:
            return AccountNameAlreadyExistsType(name=e.name)
        except custom_exceptions.AccountNotFoundException as e:
            return AccountNotFoundType(account_id=e.account_id)
        except custom_exceptions.InactiveAccountException as e:
            return InactiveAccountType(account_id=e.account_id)
        except custom_exceptions.UserNotAccountOwnerException as e:
            return UserNotAccountOwnerType(user_id=e.user_id)
        except custom_exceptions.NothingToUpdateAccountException as e:
            return NothingToUpdateAccountType(account_id=e.account_id)
