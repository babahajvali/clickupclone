from typing import Optional

from task_management.interactors.accounts.validator.account_validator import \
    AccountValidator
from task_management.interactors.dtos import AccountDTO
from task_management.interactors.storage_interfaces import \
    AccountStorageInterface, UserStorageInterface
from task_management.mixins import UserValidationMixin


class CreateAccountInteractor:

    def __init__(self, account_storage: AccountStorageInterface,
                 user_storage: UserStorageInterface):
        self.account_storage = account_storage
        self.user_storage = user_storage

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

        self.check_account_name_is_not_empty(account_name=name)
        self.user_mixin.check_user_is_active(user_id=created_by)
        self.account_validator.check_account_name_in_db(
            account_name=name, account_id=None)

        return self.account_storage.create_account(
            name=name, description=description, created_by=created_by)
