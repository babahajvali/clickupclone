from task_management.interactors.dtos import AccountDTO
from task_management.interactors.storage_interfaces import \
    AccountStorageInterface


class GetAccountsInteractor:
    """
    Account management class
    create accounts, update accounts, delete accounts, deactivate accounts, get accounts
    storages:
    account_storage for modifying the accounts data
    user_storage for validating the user related data
    Validating the Input data
    """

    def __init__(self, account_storage: AccountStorageInterface):
        self.account_storage = account_storage

    def get_accounts(self, account_ids: list[str]) -> list[AccountDTO]:
        """ Get accounts data after validations
        1. Validate the account_ids
        Args:
            account_ids
        Return:
            Accounts Data
        Exceptions:
            InvalidAccountIdsFoundException: If the accounts does not exist.
        """
        self._check_account_ids(account_ids=account_ids)

        return self.account_storage.get_accounts(account_ids=account_ids)

    def _check_account_ids(self, account_ids: list[str]):
        from task_management.exceptions.custom_exceptions import \
            InvalidAccountIds

        existed_account_ids = self.account_storage.get_existing_account_ids(
            account_ids=account_ids)
        invalid_account_ids = [account_id for account_id in account_ids if
                               account_id not in existed_account_ids]

        if invalid_account_ids:
            raise InvalidAccountIds(
                account_ids=invalid_account_ids)
