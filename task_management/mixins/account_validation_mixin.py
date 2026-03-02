from task_management.exceptions.custom_exceptions import \
    AccountNotFound, InactiveAccount, UserNotAccountOwner
from task_management.interactors.dtos import AccountDTO
from task_management.interactors.storage_interfaces.account_storage_interface import \
    AccountStorageInterface


class AccountValidationMixin:
    def __init__(self, account_storage: AccountStorageInterface):
        self.account_storage = account_storage

    def check_account_is_active(self, account_id: str):

        account_data = self.validate_account_exists(account_id=account_id)

        is_account_inactive = not account_data.is_active
        if is_account_inactive:
            raise InactiveAccount(account_id=account_id)

    def check_user_is_account_owner(self, user_id: str, account_id: str):

        account_data = self.account_storage.get_account(account_id=account_id)

        is_not_account_owner = str(account_data.owner_id) != user_id
        if is_not_account_owner:
            raise UserNotAccountOwner(user_id=user_id)

    def validate_account_exists(self, account_id: str) -> AccountDTO:

        account_data = self.account_storage.get_account(account_id=account_id)

        is_account_not_found = not account_data

        if is_account_not_found:
            raise AccountNotFound(account_id=account_id)

        return account_data
