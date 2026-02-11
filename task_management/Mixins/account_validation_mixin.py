from task_management.exceptions.custom_exceptions import \
    AccountNotFoundException, InactiveAccountException, \
    UserNotAccountOwnerException
from task_management.interactors.storage_interface.account_storage_interface import \
    AccountStorageInterface


class AccountValidationMixin:
    def __init__(self, account_storage: AccountStorageInterface, **kwargs):
        self.account_storage = account_storage
        super().__init__(**kwargs)

    def validate_account_exists(self, account_id: str):

        is_exists = self.account_storage.get_account_by_id(account_id=account_id)

        if not is_exists:
            raise AccountNotFoundException(account_id=account_id)

    def validate_account_is_active(self, account_id: str):

        account_data = self.account_storage.get_account_by_id(account_id=account_id)
        if not account_data.is_active:
            raise InactiveAccountException(account_id=account_id)

    def validate_user_is_account_owner(self, user_id: str,account_id: str):

        account_data = self.account_storage.get_account_by_id(account_id=account_id)

        if str(account_data.owner_id) != user_id:
            raise UserNotAccountOwnerException(user_id=user_id)


