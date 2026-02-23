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

    def check_account_ids(self, account_ids: list[str]):
        from task_management.exceptions.custom_exceptions import \
            InvalidAccountIds

        existed_account_ids = self.account_storage.get_existing_account_ids(
            account_ids=account_ids)
        invalid_account_ids = [account_id for account_id in account_ids if
                               account_id not in existed_account_ids]

        if invalid_account_ids:
            raise InvalidAccountIds(
                account_ids=invalid_account_ids)

    @staticmethod
    def check_account_name_is_not_empty(account_name: str):
        from task_management.exceptions.custom_exceptions import \
            EmptyAccountName
        is_name_empty = not account_name or not account_name.strip()

        if is_name_empty:
            raise EmptyAccountName(account_name=account_name)

    def check_update_account_field_properties(
            self, account_id: str, name: Optional[str],
            description: Optional[str]):
        from task_management.exceptions.custom_exceptions import \
            NothingToUpdateAccount

        is_name_provided = name is not None
        if is_name_provided:
            self.check_account_name_in_db(
                account_id=account_id, account_name=name)

        is_description_provided = description is not None

        if not(is_description_provided or is_name_provided):
            raise NothingToUpdateAccount(account_id=account_id)
