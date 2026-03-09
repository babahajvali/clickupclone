from typing import Optional

from task_management.exceptions.custom_exceptions import \
    AccountNotFound, InactiveAccount, UserNotAccountOwner, \
    AccountNameAlreadyExists
from task_management.interactors.dtos import AccountDTO
from task_management.interactors.storage_interfaces.account_storage_interface import \
    AccountStorageInterface


class AccountValidationMixin:
    def __init__(self, account_storage: AccountStorageInterface, **kwargs):
        self.account_storage = account_storage
        super().__init__(**kwargs)

    def check_account_is_active(self, account_id: str):

        account_data = self.check_account_exists(account_id=account_id)

        is_account_inactive = not account_data.is_active
        if is_account_inactive:
            raise InactiveAccount(account_id=account_id)

    def check_user_is_account_owner(self, user_id: str, account_id: str):

        account_data = self.account_storage.get_account(account_id=account_id)

        is_not_account_owner = str(account_data.owner_id) != user_id
        if is_not_account_owner:
            raise UserNotAccountOwner(user_id=user_id)

    def check_account_exists(self, account_id: str) -> AccountDTO:

        account_data = self.account_storage.get_account(account_id=account_id)

        is_account_not_found = not account_data

        if is_account_not_found:
            raise AccountNotFound(account_id=account_id)

        return account_data

    def check_account_name_in_db(
            self, account_name: str, account_id: Optional[str]):
        is_account_name_exist = self.account_storage.is_account_name_exists(
            account_name=account_name, excluded_account_id=account_id)

        if is_account_name_exist:
            raise AccountNameAlreadyExists(name=account_name)

    @staticmethod
    def check_account_name_is_not_empty(account_name: str):
        from task_management.exceptions.custom_exceptions import \
            EmptyAccountName
        is_name_empty = not account_name or not account_name.strip()

        if is_name_empty:
            raise EmptyAccountName(account_name=account_name)
