from task_management.exceptions.custom_exceptions import \
    AlreadyAccountNameExistedException, UserNotAccountOwnerException
from task_management.interactors.dtos import CreateAccountDTO, AccountDTO
from task_management.interactors.storage_interface.account_storage_interface import \
    AccountStorageInterface
from task_management.interactors.storage_interface.account_member_storage_interface import \
    AccountMemberStorageInterface
from task_management.interactors.storage_interface.user_storage_interface import \
    UserStorageInterface
from task_management.interactors.validation_mixin import ValidationMixin


class AccountInteractor(ValidationMixin):
    def __init__(self, account_storage_interface: AccountStorageInterface,
                 user_storage: UserStorageInterface,
                 account_user_storage: AccountMemberStorageInterface):
        self.account_storage = account_storage_interface
        self.user_storage = user_storage
        self.account_user_storage = account_user_storage

    def create_account(self,
                       create_account_data: CreateAccountDTO) -> AccountDTO:
        self._validate_account_name_exists(
            account_name=create_account_data.name)

        return self.account_storage.create_account(create_account_data)

    def transfer_account(self, account_id: str, old_owner_id: str,
                         new_owner_id: str) -> AccountDTO:
        self.validate_account_is_active(account_id=account_id,
                                        account_storage=self.account_storage)
        self._validate_user_is_account_owner(account_id=account_id,
                                             user_id=old_owner_id)
        self.validate_user_is_active(user_id=new_owner_id,
                                     user_storage=self.user_storage)

        return self.account_storage.transfer_account(account_id=account_id,
                                                     new_owner_id=new_owner_id)

    def delete_account(self, account_id: str, deleted_by: str):
        self.validate_account_is_active(account_id=account_id,
                                        account_storage=self.account_storage)
        self.validate_user_access_for_account(
            account_id=account_id, user_id=deleted_by,
            account_member_storage=self.account_user_storage)

        return self.account_storage.delete_account(account_id=account_id)

    # Helping functions

    def _validate_account_name_exists(self, account_name: str):
        is_name_exist = self.account_storage.validate_account_name_exists(
            name=account_name)

        if is_name_exist:
            raise AlreadyAccountNameExistedException(name=account_name)

    def _validate_user_is_account_owner(self, user_id: str, account_id: str):
        account_data = self.account_storage.get_account_by_id(
            account_id=account_id)

        if account_data.owner_id != user_id:
            raise UserNotAccountOwnerException(user_id=user_id)
