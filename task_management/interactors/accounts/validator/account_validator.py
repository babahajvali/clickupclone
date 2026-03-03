from typing import Optional

from task_management.exceptions.custom_exceptions import \
    AccountNameAlreadyExists
from task_management.interactors.storage_interfaces import \
    AccountStorageInterface


class AccountValidator:

    def __init__(self, account_storage: AccountStorageInterface):
        self.account_storage = account_storage

    def check_account_name_in_db(self, account_name: str,
                                 account_id: Optional[str]):
        is_account_name_exist = self.account_storage.is_account_name_exists(
            account_name=account_name, account_id=account_id)

        if is_account_name_exist:
            raise AccountNameAlreadyExists(name=account_name)
