from abc import ABC, abstractmethod

from task_management.interactors.dtos import AccountDTO, CreateAccountDTO, \
    UpdateAccountDTO


class AccountStorageInterface(ABC):

    @abstractmethod
    def get_account_by_id(self, account_id: str) -> AccountDTO:
        pass

    @abstractmethod
    def validate_account_name_exists(self, name: str) -> bool:
        pass

    @abstractmethod
    def create_account(self, account_dto: CreateAccountDTO) -> AccountDTO:
        pass

    @abstractmethod
    def transfer_account(self, account_id: str,
                         new_owner_id: str) -> AccountDTO:
        pass

    @abstractmethod
    def delete_account(self, account_id: str) -> AccountDTO:
        # soft delete change the is_active is False
        pass

    @abstractmethod
    def get_accounts(self,account_ids: list[str]) -> list[AccountDTO]:
        pass


    @abstractmethod
    def get_user_accounts(self, user_id: str) -> list[AccountDTO]:
        pass

    @abstractmethod
    def validate_account_name_except_current(self,name: str, account_id: str) -> bool:
        pass


    @abstractmethod
    def update_account(self, update_data: UpdateAccountDTO) -> AccountDTO:
        pass