from task_management.graphql.types.types import AccountType, AccountsType
from task_management.storages import AccountStorage


def get_user_accounts_resolver(root, info):
    account_storage = AccountStorage()

    user_id = info.context.user_id

    accounts_data = account_storage.get_user_accounts(user_id=user_id)

    results = [AccountType(
        account_id=result.account_id,
        name=result.name,
        description=result.description,
        owner_id=result.owner_id,
        is_active=result.is_active,
    ) for result in accounts_data]

    return AccountsType(accounts=results)
