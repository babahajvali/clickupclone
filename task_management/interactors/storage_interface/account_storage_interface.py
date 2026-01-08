from abc import ABC, abstractmethod

from task_management.interactors.dtos import AccountDTO, CreateAccountDTO


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
