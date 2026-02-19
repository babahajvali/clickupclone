from typing import Optional

from task_management.interactors.dtos import AccountDTO
from task_management.interactors.storage_interfaces import \
    AccountStorageInterface, UserStorageInterface

from task_management.mixins import AccountValidationMixin, UserValidationMixin


class AccountInteractor(AccountValidationMixin, UserValidationMixin):
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

        self.check_user_is_active(user_id=created_by)
        self.check_account_name_is_not_empty(account_name=name)
        self.check_account_name_in_db(account_name=name)

        return self.account_storage.create_account(
            name=name, description=description, created_by=created_by)

    def update_account(self, account_id: str, user_id: str,
                       name: Optional[str],
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

        self.check_account_is_active(account_id=account_id)
        field_properties_to_update = self.check_update_account_field_properties(
            account_id=account_id, name=name, description=description)

        self.check_user_is_account_owner(
            user_id=user_id, account_id=account_id)

        return self.account_storage.update_account(
            account_id=account_id, field_properties=field_properties_to_update)

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

        self.check_account_is_active(account_id=account_id)
        self.check_user_is_account_owner(
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

        self.check_account_is_active(account_id=account_id)
        self.check_user_is_account_owner(account_id=account_id,
                                         user_id=deactivated_by)

        return self.account_storage.deactivate_account(account_id=account_id)

    def get_accounts(self, account_ids: list[str]) -> list[AccountDTO]:
        """ Get account data after validations
        1. Validate the account_ids
        Args:
            account_ids
        Return:
            Accounts Data
        Exceptions:
            InvalidAccountIdsFoundException: If the account does not exist.
            """
        self.check_account_ids(account_ids=account_ids)

        return self.account_storage.get_accounts(account_ids=account_ids)

    # Helping functions

    def check_update_account_field_properties(
            self, account_id: str, name: Optional[str],
            description: Optional[str]) -> dict:

        field_properties_to_update = {}
        is_name_provided = name is not None
        if is_name_provided:
            self.check_account_name_in_db_except_current_account(
                account_id=account_id, name=name)
            field_properties_to_update['name'] = name

        is_description_provided = description is not None
        if is_description_provided:
            field_properties_to_update['description'] = description

        if not field_properties_to_update:
            from task_management.exceptions.custom_exceptions import \
                NothingToUpdateAccountException
            raise NothingToUpdateAccountException(account_id=account_id)

        return field_properties_to_update
