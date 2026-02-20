from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import InvalidAccountIdsType

from task_management.graphql.types.types import AccountsType, AccountType
from task_management.interactors.accounts.account_interactor import \
    AccountInteractor
from task_management.storages import AccountStorage, UserStorage


def get_accounts_resolver(root, info, params):
    account_ids = params.account_ids
    account_storage = AccountStorage()
    user_storage = UserStorage()

    account_interactor = AccountInteractor(account_storage=account_storage,
                                           user_storage=user_storage)

    try:
        accounts_data = account_interactor.get_accounts(account_ids=account_ids)
        results = [AccountType(
            account_id=result.account_id,
            name=result.name,
            description=result.description,
            owner_id=result.owner_id,
            is_active=result.is_active,
        ) for result in accounts_data]

        return AccountsType(accounts=results)
    except custom_exceptions.InvalidAccountIds as e:
        return InvalidAccountIdsType(account_ids=e.account_ids)
