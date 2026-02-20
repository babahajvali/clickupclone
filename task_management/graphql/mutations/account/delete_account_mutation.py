import graphene

from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import AccountNotFoundType, \
    InactiveAccountType, ModificationNotAllowedType
from task_management.graphql.types.input_types import DeleteAccountInputParams
from task_management.graphql.types.response_types import DeleteAccountResponse
from task_management.graphql.types.types import AccountType
from task_management.interactors.accounts.account_interactor import \
    AccountInteractor
from task_management.storages import UserStorage, AccountStorage


class DeleteAccountMutation(graphene.Mutation):
    class Arguments:
        params = DeleteAccountInputParams(required=True)

    Output = DeleteAccountResponse

    @staticmethod
    def mutate(root, info, params):
        account_id = params.account_id
        deleted_by = info.context.user_id

        user_storage = UserStorage()
        account_storage = AccountStorage()

        interactor = AccountInteractor(
            user_storage=user_storage,
            account_storage=account_storage)

        try:
            result = interactor.delete_account(
                account_id=account_id,
                deleted_by=deleted_by
            )

            return AccountType(
                account_id=result.account_id,
                name=result.name,
                description=result.description,
                owner_id=result.owner_id,
                is_active=result.is_active,
            )

        except custom_exceptions.AccountNotFound as e:
            return AccountNotFoundType(account_id=e.account_id)

        except custom_exceptions.InactiveAccount as e:
            return InactiveAccountType(account_id=e.account_id)

        except custom_exceptions.ModificationNotAllowed as e:
            return ModificationNotAllowedType(user_id=e.user_id)
