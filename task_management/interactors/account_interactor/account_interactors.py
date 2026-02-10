from task_management.exceptions.custom_exceptions import \
    AccountNameAlreadyExistsException, InvalidAccountIdsException, \
    InactiveAccountIdsException
from task_management.interactors.account_interactor.account_onboarding import \
    AccountOnboardingHandler
from task_management.interactors.dtos import CreateAccountDTO, AccountDTO, \
    UpdateAccountDTO
from task_management.interactors.storage_interface.account_storage_interface import \
    AccountStorageInterface
from task_management.interactors.storage_interface.user_storage_interface import \
    UserStorageInterface
from task_management.interactors.validation_mixin import ValidationMixin


class AccountInteractor(ValidationMixin):
    def __init__(self, account_storage: AccountStorageInterface,
                 user_storage: UserStorageInterface,
                 account_onboarding: AccountOnboardingHandler = None):
        self.account_storage = account_storage
        self.user_storage = user_storage
        self.account_onboarding = account_onboarding

    def create_account(self,
                       create_account_data: CreateAccountDTO) -> AccountDTO:
        self._validate_account_name_exists(
            account_name=create_account_data.name)

        result = self.account_storage.create_account(create_account_data)
        if self.account_onboarding:
            self.account_onboarding.create_default_workspace(
                account_id=result.account_id,
                owner_id=result.owner_id, name=result.name)

        return result

    def update_account(self, update_data: UpdateAccountDTO,
                       user_id: str) -> AccountDTO:
        self.validate_account_is_active(account_id=update_data.account_id,
                                        account_storage=self.account_storage)
        self.validate_user_is_account_owner(user_id=user_id,
                                            account_id=update_data.account_id,
                                            account_storage=self.account_storage)
        if update_data.name is not None:
            self._validate_account_name_except_current(
                account_id=update_data.account_id, name=update_data.name)

        return self.account_storage.update_account(update_data=update_data)

    def transfer_account(self, account_id: str, current_owner_id: str,
                         new_owner_id: str) -> AccountDTO:
        self.validate_account_is_active(account_id=account_id,
                                        account_storage=self.account_storage)
        self.validate_user_is_account_owner(
            account_id=account_id, user_id=current_owner_id,
            account_storage=self.account_storage)
        self.validate_user_is_active(user_id=new_owner_id,
                                     user_storage=self.user_storage)

        return self.account_storage.transfer_account(account_id=account_id,
                                                     new_owner_id=new_owner_id)

    def delete_account(self, account_id: str, deleted_by: str):
        self.validate_account_is_active(account_id=account_id,
                                        account_storage=self.account_storage)

        self.validate_user_is_account_owner(
            account_id=account_id, user_id=deleted_by,
            account_storage=self.account_storage)

        return self.account_storage.delete_account(account_id=account_id)

    def get_accounts(self, account_ids: list[str]) -> list[AccountDTO]:
        accounts_data = self._check_accounts_active(account_ids=account_ids)

        return accounts_data

    # Helping functions

    def _validate_account_name_exists(self, account_name: str):
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
