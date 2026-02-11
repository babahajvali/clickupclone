from typing import Optional

from task_management.Mixins.account_validation_mixin import \
    AccountValidationMixin
from task_management.Mixins.user_validation_mixin import UserValidationMixin
from task_management.exceptions.custom_exceptions import \
    AccountNameAlreadyExistsException, InvalidAccountIdsException, \
    InactiveAccountIdsException, EmptyAccountNameException

from task_management.interactors.dtos import AccountDTO, UpdateAccountDTO
from task_management.interactors.storage_interface.account_storage_interface import \
    AccountStorageInterface
from task_management.interactors.storage_interface.user_storage_interface import \
    UserStorageInterface


class Account(AccountValidationMixin, UserValidationMixin):
    '''
    Account management class
    create account, update account, delete account, deactivate account, get accounts
    storages:
    account_storage for modifying the account data
    user_storage for validating the user related data'''
    def __init__(self, account_storage: AccountStorageInterface,
                 user_storage: UserStorageInterface):
        super().__init__(account_storage=account_storage,
                         user_storage=user_storage)
        self.account_storage = account_storage
        self.user_storage = user_storage

    def create_account(self, name: str, description: Optional[str],
                       created_by: str) -> AccountDTO:
        """ Create new account after validations
        Validate input data
            1. validate account name
            2. validate user

        Args:
             name: account name
             description: account description
             created_by: account created by

        Returns:
            AccountDTO: The newly created account data

        Exceptions:
            UserNotFoundException: If the user does not exist.
            InactiveUserException: If the user is not active.
            EmptyAccountNameException: If the account name is empty.
            AccountNameAlreadyExistsException: If the account name is already taken.
        """

        self.validate_user_exists(user_id=created_by)
        self.validate_user_is_active(user_id=created_by)
        self._validate_account_name_not_empty(account_name=name)
        self._validate_account_name_already_exists(account_name=name)

        return self.account_storage.create_account(
            name=name, description=description, created_by=created_by)

    def update_account(self, update_data: UpdateAccountDTO,
                       user_id: str) -> AccountDTO:

        self.validate_account_exists(account_id=update_data.account_id)
        self.validate_account_is_active(account_id=update_data.account_id)

        self.validate_user_is_account_owner(
            user_id=user_id, account_id=update_data.account_id)
        if update_data.name:
            self._validate_account_name_except_current(
                account_id=update_data.account_id, name=update_data.name)

        return self.account_storage.update_account(update_data=update_data)

    def delete_account(self, account_id: str, deleted_by: str):

        self.validate_account_exists(account_id=account_id)
        self.validate_account_is_active(account_id=account_id)

        self.validate_user_is_account_owner(
            account_id=account_id, user_id=deleted_by)

        return self.account_storage.delete_account(account_id=account_id)

    def deactivate_account(self, account_id: str, deactivated_by: str):

        self.validate_account_exists(account_id=account_id)
        self.validate_account_is_active(account_id=account_id)
        self.validate_user_is_account_owner(account_id=account_id,
                                            user_id=deactivated_by)

        return self.account_storage.deactivate_account(account_id=account_id, )

    def get_accounts(self, account_ids: list[str]) -> list[AccountDTO]:
        accounts_data = self._check_accounts_active(account_ids=account_ids)

        return accounts_data

    # Helping functions

    def _validate_account_name_already_exists(self, account_name: str):
        is_name_exist = self.account_storage.validate_account_name_exists(
            name=account_name)

        if is_name_exist:
            raise AccountNameAlreadyExistsException(name=account_name)

    def _validate_account_name_except_current(self, name: str,
                                              account_id: str):
        is_name_exist = self.account_storage.validate_account_name_except_current(
            name=name, account_id=account_id)

        if is_name_exist:
            raise AccountNameAlreadyExistsException(name=name)

    def _check_accounts_active(self, account_ids: list[str]):
        accounts_data = self.account_storage.get_accounts(
            account_ids=account_ids)

        existed_active_account_ids = [str(obj.account_id) for obj in
                                      accounts_data if obj.is_active]
        existed_inactive_account_ids = [str(obj.account_id) for obj in
                                        accounts_data if not obj.is_active]
        invalid_accounts_ids = []
        inactive_accounts_ids = []

        for account_id in account_ids:
            if account_id not in existed_active_account_ids and account_id not in existed_inactive_account_ids:
                invalid_accounts_ids.append(account_id)
            elif account_id in existed_inactive_account_ids:
                inactive_accounts_ids.append(account_id)

        if invalid_accounts_ids:
            raise InvalidAccountIdsException(
                account_ids=invalid_accounts_ids)

        if inactive_accounts_ids:
            raise InactiveAccountIdsException(
                account_ids=inactive_accounts_ids)

        return accounts_data

    @staticmethod
    def _validate_account_name_not_empty(account_name: str):
        if not account_name:
            raise EmptyAccountNameException(name=account_name)
