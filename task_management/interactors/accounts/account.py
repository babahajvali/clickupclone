from typing import Optional

from task_management.Mixins.account_validation_mixin import \
    AccountValidationMixin
from task_management.Mixins.user_validation_mixin import UserValidationMixin

from task_management.interactors.dtos import AccountDTO
from task_management.interactors.storage_interface.account_storage_interface import \
    AccountStorageInterface
from task_management.interactors.storage_interface.user_storage_interface import \
    UserStorageInterface


class Account(AccountValidationMixin, UserValidationMixin):
    """
    Account management class
    create account, update account, delete account, deactivate account, get accounts
    storages:
    account_storage for modifying the account data
    user_storage for validating the user related data
    Validating the Input data """

    def __init__(self, account_storage: AccountStorageInterface,
                 user_storage: UserStorageInterface):
        super().__init__(account_storage=account_storage,
                         user_storage=user_storage)
        self.account_storage = account_storage
        self.user_storage = user_storage

    def create_account(self, name: str, created_by: str,
                       description: Optional[str]) -> AccountDTO:
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

    def update_account(self, account_id: str, user_id: str, name: Optional[str],
                       description: Optional[str]) -> AccountDTO:
        """ Update account data after validations
        validate input data
            1. validate account name
            2. validate user
            3. update account data
            4. pass the only updated data
        Args:
            1.account_id: account id
            2.account_name: account name optional
            3.description: account description optional
        """

        self.validate_account_exists(account_id=account_id)
        self.validate_account_is_active(account_id=account_id)

        self.validate_user_is_account_owner(
            user_id=user_id, account_id=account_id)

        fields_to_update = {}
        if name:
            self._validate_account_name_except_current(
                account_id=account_id, name=name)
            fields_to_update['name'] = name
        if description:
            fields_to_update['description'] = description

        if not fields_to_update:
            from task_management.exceptions.custom_exceptions import \
                NothingToUpdateException
            raise NothingToUpdateException(account_id=account_id)

        return self.account_storage.update_account(account_id=account_id,
                                                   update_fields=fields_to_update)

    def delete_account(self, account_id: str, deleted_by: str):
        """ Delete account data after validation
        Validations:
            1. validate account
            2. validate account is active
            3. validate user is owner of account

        Args:
            1.account_id: account id
            2.deleted_by: account deleted by

        Exceptions:
            1.AccountDoesNotExistException: If the account does not exist.
            2.UserNotOwnerOfAccountException: If the user is not owner of account.
            3.InactiveAccountException: If the account is not active.
            """

        self.validate_account_exists(account_id=account_id)
        self.validate_account_is_active(account_id=account_id)

        self.validate_user_is_account_owner(
            account_id=account_id, user_id=deleted_by)

        return self.account_storage.delete_account(account_id=account_id)

    def deactivate_account(self, account_id: str, deactivated_by: str):
        """ Deactivate account after validation
                Validations:
                    1. validate account
                    2. validate account is active
                    3. validate user is owner of account

                Args:
                    1.account_id: account id
                    2.deactivated_by: account deleted by

                Exceptions:
                    1.AccountDoesNotExistException: If the account does not exist.
                    2.UserNotOwnerOfAccountException: If the user is not owner of account.
                    3.InactiveAccountException: If the account is not active.
                    """

        self.validate_account_exists(account_id=account_id)
        self.validate_account_is_active(account_id=account_id)
        self.validate_user_is_account_owner(account_id=account_id,
                                            user_id=deactivated_by)

        return self.account_storage.deactivate_account(account_id=account_id, )

    def get_accounts(self, account_ids: list[str]) -> list[AccountDTO]:
        """ Get accounts data after validations
        1. Validate the account_ids
        Args:
            account_ids
        Return:
            Accounts Data
        Exceptions:
            InvalidAccountIdsFoundException: If the account does not exist.
            """
        accounts_data = self._check_accounts_active(account_ids=account_ids)

        return accounts_data

    # Helping functions

    def _validate_account_name_already_exists(self, account_name: str):
        is_name_exist = self.account_storage.validate_account_name_exists(
            name=account_name)

        if is_name_exist:
            from task_management.exceptions.custom_exceptions import \
                AccountNameAlreadyExistsException
            raise AccountNameAlreadyExistsException(name=account_name)

    def _validate_account_name_except_current(self, name: str,
                                              account_id: str):
        is_name_exist = self.account_storage.validate_account_name_except_current(
            name=name, account_id=account_id)

        if is_name_exist:
            from task_management.exceptions.custom_exceptions import \
                AccountNameAlreadyExistsException
            raise AccountNameAlreadyExistsException(name=name)

    def _check_accounts_active(self, account_ids: list[str]):
        accounts_data = self.account_storage.get_accounts(
            account_ids=account_ids)

        existed_account_ids = [str(obj.account_id) for obj in accounts_data]
        invalid_accounts_ids = []

        for account_id in account_ids:
            if account_id not in existed_account_ids:
                invalid_accounts_ids.append(account_id)

        if invalid_accounts_ids:
            from task_management.exceptions.custom_exceptions import \
                InvalidAccountIdsException
            raise InvalidAccountIdsException(
                account_ids=invalid_accounts_ids)

        return accounts_data

    @staticmethod
    def _validate_account_name_not_empty(account_name: str):
        if not account_name or not account_name.strip():
            from task_management.exceptions.custom_exceptions import \
                EmptyAccountNameException
            raise EmptyAccountNameException(name=account_name)
