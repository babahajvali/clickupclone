from typing import Optional

from task_management.exceptions.custom_exceptions import \
    AccountNameAlreadyExists
from task_management.interactors.storage_interfaces import \
    AccountStorageInterface


class AccountValidator:

    def __init__(self, account_storage: AccountStorageInterface):
        self.account_storage = account_storage

    def check_account_name_in_db(self, account_name: str):

        is_account_name_exist = self.account_storage.is_name_exists(
            account_name=account_name, account_id=None)

        if is_account_name_exist:
            raise AccountNameAlreadyExists(name=account_name)

    def check_name_in_db_except_current_account(self, name: str,
                                                account_id: str):
        is_account_name_exist = self.account_storage.is_name_exists(
            account_name=name, account_id=account_id)

        if is_account_name_exist:
            raise AccountNameAlreadyExists(name=name)

    def check_account_ids(self, account_ids: list[str]):
        accounts_data = self.account_storage.get_accounts(
            account_ids=account_ids)

        existed_account_ids = [str(obj.account_id) for obj in accounts_data]
        invalid_account_ids = [account_id for account_id in account_ids if
                               account_id not in existed_account_ids]

        if invalid_account_ids:
            from task_management.exceptions.custom_exceptions import \
                InvalidAccountIds
            raise InvalidAccountIds(
                account_ids=invalid_account_ids)

    @staticmethod
    def check_account_name_is_not_empty(account_name: str):
        is_name_empty = not account_name or not account_name.strip()

        if is_name_empty:
            from task_management.exceptions.custom_exceptions import \
                EmptyName
            raise EmptyName(name=account_name)


    def check_update_account_field_properties(
            self, account_id: str, name: Optional[str],
            description: Optional[str]) -> dict:

        field_properties_to_update = {}
        is_name_provided = name is not None
        if is_name_provided:
            self.check_name_in_db_except_current_account(
                account_id=account_id, name=name)
            field_properties_to_update['name'] = name

        is_description_provided = description is not None
        if is_description_provided:
            field_properties_to_update['description'] = description

        if not field_properties_to_update:
            from task_management.exceptions.custom_exceptions import \
                NothingToUpdateAccount
            raise NothingToUpdateAccount(account_id=account_id)

        return field_properties_to_update
