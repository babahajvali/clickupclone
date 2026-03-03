from typing import Optional

from task_management.interactors.accounts.validator.account_validator import \
    AccountValidator
from task_management.interactors.dtos import AccountDTO
from task_management.interactors.storage_interfaces import \
    AccountStorageInterface
from task_management.mixins import AccountValidationMixin


class UpdateAccountInteractor:

    def __init__(self, account_storage: AccountStorageInterface):
        self.account_storage = account_storage

    @property
    def account_mixin(self) -> AccountValidationMixin:
        return AccountValidationMixin(account_storage=self.account_storage)

    @property
    def account_validator(self) -> AccountValidator:
        return AccountValidator(account_storage=self.account_storage)

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

        self._check_update_account_field_properties(
            account_id=account_id, name=name, description=description)
        self.account_mixin.check_account_is_active(account_id=account_id)
        self.account_mixin.check_user_is_account_owner(
            user_id=user_id, account_id=account_id
        )

        return self.account_storage.update_account(
            account_id=account_id, name=name, description=description
        )

    def _check_update_account_field_properties(
            self, account_id: str, name: Optional[str],
            description: Optional[str]):
        from task_management.exceptions.custom_exceptions import \
            NothingToUpdateAccount

        is_name_provided = name is not None
        is_description_provided = description is not None

        has_no_update_field_properties = any([
            is_description_provided,
            is_name_provided
        ])

        if has_no_update_field_properties:
            raise NothingToUpdateAccount(account_id=account_id)

        if is_name_provided:
            self.account_validator.check_account_name_is_not_empty(
                account_name=name)
            self.account_validator.check_account_name_in_db(
                account_id=account_id, account_name=name)
