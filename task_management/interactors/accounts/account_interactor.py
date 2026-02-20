from typing import Optional

from task_management.interactors.accounts.validator.account_validator import \
    AccountValidator
from task_management.interactors.dtos import AccountDTO
from task_management.interactors.storage_interfaces import \
    AccountStorageInterface, UserStorageInterface

from task_management.mixins import AccountValidationMixin, UserValidationMixin


class AccountInteractor:
    """
    Account management class
    create accounts, update accounts, delete accounts, deactivate accounts, get accounts
    storages:
    account_storage for modifying the accounts data
    user_storage for validating the user related data
    Validating the Input data """

    def __init__(self, account_storage: AccountStorageInterface,
                 user_storage: UserStorageInterface):
        self.account_storage = account_storage
        self.user_storage = user_storage

    @property
    def account_mixin(self) -> AccountValidationMixin:
        return AccountValidationMixin(account_storage=self.account_storage)

    @property
    def user_mixin(self) -> UserValidationMixin:
        return UserValidationMixin(user_storage=self.user_storage)

    @property
    def account_validator(self) -> AccountValidator:
        return AccountValidator(account_storage=self.account_storage)

    def create_account(
            self, name: str, created_by: str, description: Optional[str]) \
            -> AccountDTO:
        """ Create new accounts after validations
        Validate input data
            1. validate accounts name
            2. validate user

        Args:
             name: accounts name
             description: accounts description
             created_by: accounts created by

        Returns:
            AccountDTO: The newly created accounts data

        Exceptions:
            UserNotFoundException: If the user does not exist.
            InactiveUserException: If the user is not active.
            EmptyAccountNameException: If the accounts name is empty.
            AccountNameAlreadyExistsException: If the accounts name is already taken.
        """

        self.user_mixin.check_user_is_active(user_id=created_by)
        self.account_validator.check_account_name_is_not_empty(
            account_name=name)
        self.account_validator.check_account_name_in_db(account_name=name)

        return self.account_storage.create_account(
            name=name, description=description, created_by=created_by)

    def update_account(
            self, account_id: str, user_id: str,
            name: Optional[str], description: Optional[str]) \
            -> AccountDTO:
        """ Update accounts data after validations
        validate input data
            1. validate accounts name
            2. validate user
            3. update accounts data
            4. pass the only updated data
        Args:
            1.account_id: accounts id
            2.account_name: accounts name optional
            3.description: accounts description optional
        """

        self.account_mixin.check_account_is_active(account_id=account_id)
        field_properties_to_update = (
            self.account_validator.check_update_account_field_properties(
            account_id=account_id, name=name, description=description))

        self.account_mixin.check_user_is_account_owner(
            user_id=user_id, account_id=account_id
        )

        return self.account_storage.update_account(
            account_id=account_id, field_properties=field_properties_to_update
        )

    def delete_account(self, account_id: str, deleted_by: str):
        """ Delete accounts data after validation
        Validations:
            1. validate accounts
            2. validate accounts is active
            3. validate user is owner of accounts

        Args:
            1.account_id: accounts id
            2.deleted_by: accounts deleted by

        Exceptions:
            1.AccountDoesNotExistException: If the accounts does not exist.
            2.UserNotOwnerOfAccountException: If the user is not owner of accounts.
            3.InactiveAccountException: If the accounts is not active.
            """

        self.account_mixin.check_account_is_active(account_id=account_id)
        self.account_mixin.check_user_is_account_owner(
            account_id=account_id, user_id=deleted_by)

        return self.account_storage.delete_account(account_id=account_id)

    def deactivate_account(self, account_id: str, deactivated_by: str):
        """ Deactivate accounts after validation
            Validations:
                1. validate accounts
                2. validate accounts is active
                3. validate user is owner of accounts

            Args:
                1.account_id: accounts id
                2.deactivated_by: accounts deleted by

            Exceptions:
                1.AccountDoesNotExistException: If the accounts does not exist.
                2.UserNotOwnerOfAccountException: If the user is not owner of accounts.
                3.InactiveAccountException: If the accounts is not active.
        """

        self.account_mixin.check_account_is_active(account_id=account_id)
        self.account_mixin.check_user_is_account_owner(
            account_id=account_id, user_id=deactivated_by
        )

        return self.account_storage.deactivate_account(account_id=account_id)

    def get_accounts(self, account_ids: list[str]) -> list[AccountDTO]:
        """ Get accounts data after validations
        1. Validate the account_ids
        Args:
            account_ids
        Return:
            Accounts Data
        Exceptions:
            InvalidAccountIdsFoundException: If the accounts does not exist.
            """
        self.account_validator.check_account_ids(account_ids=account_ids)

        return self.account_storage.get_accounts(account_ids=account_ids)
