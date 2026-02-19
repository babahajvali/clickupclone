from django.core.exceptions import ObjectDoesNotExist

from task_management.exceptions.custom_exceptions import \
    AccountNotFoundException, InactiveAccountException, \
    UserNotAccountOwnerException, AccountNameAlreadyExistsException
from task_management.interactors.storage_interfaces.account_storage_interface import \
    AccountStorageInterface


class AccountValidationMixin:
    def __init__(self, account_storage: AccountStorageInterface, **kwargs):
        self.account_storage = account_storage
        super().__init__(**kwargs)

    def check_account_is_active(self, account_id: str):

        account_data = self.account_storage.get_account_by_id(account_id=account_id)

        is_account_not_found = not account_data
        if is_account_not_found:
            raise AccountNotFoundException(account_id=account_id)

        is_account_inactive = not account_data.is_active
        if is_account_inactive:
            raise InactiveAccountException(account_id=account_id)

    def check_user_is_account_owner(self, user_id: str, account_id: str):

        account_data = self.account_storage.get_account_by_id(account_id=account_id)

        is_not_account_owner = str(account_data.owner_id) != user_id
        if is_not_account_owner:
            raise UserNotAccountOwnerException(user_id=user_id)


    def check_account_name_in_db(self, account_name: str):
        try:
            account_data = self.account_storage.get_account_by_name(
                account_name=account_name
            )
        except ObjectDoesNotExist:
            pass
        else:
            if account_data:
                raise AccountNameAlreadyExistsException(name=account_name)

    def check_account_name_in_db_except_current_account(self, name: str,
                                                        account_id: str):
        try:
            account_data = self.account_storage.get_account_by_name(
                account_name=name)
        except ObjectDoesNotExist:
            pass
        else:
            is_different_account = str(account_data) != str(account_id)
            if is_different_account:
                raise AccountNameAlreadyExistsException(name=name)

    def check_account_ids(self, account_ids: list[str]):
        accounts_data = self.account_storage.get_accounts(
            account_ids=account_ids)

        existed_account_ids = [str(obj.account_id) for obj in accounts_data]
        invalid_account_ids = [account_id for account_id in account_ids if
                               account_id not in existed_account_ids]

        if invalid_account_ids:
            from task_management.exceptions.custom_exceptions import \
                InvalidAccountIdsException
            raise InvalidAccountIdsException(
                account_ids=invalid_account_ids)

    @staticmethod
    def check_account_name_is_not_empty(account_name: str):
        is_name_empty =  not account_name or not account_name.strip()

        if is_name_empty:
            from task_management.exceptions.custom_exceptions import \
                EmptyNameException
            raise EmptyNameException(name=account_name)


