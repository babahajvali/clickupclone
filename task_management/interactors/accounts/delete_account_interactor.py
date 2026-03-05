from task_management.interactors.storage_interfaces import \
    AccountStorageInterface
from task_management.mixins import AccountValidationMixin


class DeleteAccountInteractor:

    def __init__(self, account_storage: AccountStorageInterface):
        self.account_storage = account_storage

    @property
    def account_mixin(self) -> AccountValidationMixin:
        return AccountValidationMixin(account_storage=self.account_storage)

    def delete_account(self, account_id: str, deleted_by: str):
        """ Delete accounts data after validation
        Validations:
            1. validate accounts
            2. validate accounts is active
            3. validate user is owner of accounts

        Args:
            1.account_id: accounts id
            2.deleted_by: accounts deleted by

        Exceptions:
            1.AccountDoesNotExistException: If the accounts does not exist.
            2.UserNotOwnerOfAccountException: If the user is not owner of accounts.
            3.InactiveAccountException: If the accounts is not active.
        """

        self.account_mixin.check_account_exists(account_id=account_id)
        self.account_mixin.check_user_is_account_owner(
            account_id=account_id, user_id=deleted_by)

        return self.account_storage.delete_account(account_id=account_id)
