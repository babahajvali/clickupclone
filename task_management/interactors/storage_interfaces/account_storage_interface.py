from abc import ABC, abstractmethod
from typing import Optional, List

from task_management.interactors.dtos import AccountDTO


class AccountStorageInterface(ABC):

    @abstractmethod
    def get_account_by_id(self, account_id: str) -> AccountDTO:
        pass

    @abstractmethod
    def create_account(
            self, name: str, description: Optional[str], created_by: str) \
            -> AccountDTO:
        pass

    @abstractmethod
    def deactivate_account(self, account_id: str) -> AccountDTO:
        pass

    @abstractmethod
    def delete_account(self, account_id: str):
        pass

    @abstractmethod
    def get_accounts(self, account_ids: List[str]) -> List[AccountDTO]:
        pass

    @abstractmethod
    def get_existing_account_ids(self, account_ids: List[str]) -> List[str]:
        pass

    @abstractmethod
    def get_user_accounts(self, user_id: str) -> List[AccountDTO]:
        pass

    @abstractmethod
    def update_account(
            self, account_id: str, name: Optional[str],
            description: Optional[str]) -> AccountDTO:
        pass

    @abstractmethod
    def is_account_name_exists(
            self, account_name: str, account_id: Optional[str]) -> bool:
        pass
