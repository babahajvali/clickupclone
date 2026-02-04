from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import \
    InvalidAccountIdsFoundType
from task_management.graphql.types.types import AccountType, AccountsType
from task_management.storages.account_storage import AccountStorage


def get_user_accounts_resolver(root, info):
    account_storage = AccountStorage()

    try:
        user_id = info.context.user_id

        accounts_data = account_storage.get_user_accounts(user_id=user_id)

        results = [AccountType(
            account_id=result.account_id,
            name=result.name,
            description=result.description,
            owner_id=result.owner_id,
            is_active=result.is_active,
        )for result in accounts_data]

        return AccountsType(accounts=results)

    except custom_exceptions.InvalidAccountIdsFoundException as e:
        return InvalidAccountIdsFoundType(account_ids=e.account_ids)

