from abc import ABC, abstractmethod
from typing import Optional

from task_management.interactors.dtos import AccountDTO


class AccountStorageInterface(ABC):

    @abstractmethod
    def get_account_by_id(self, account_id: str) -> AccountDTO:
        pass

    @abstractmethod
    def validate_account_name_exists(self, name: str) -> bool:
        pass

    @abstractmethod
    def create_account(
            self, name: str, description: Optional[str], created_by: str)\
            -> AccountDTO:
        pass

    @abstractmethod
    def deactivate_account(self, account_id: str) -> AccountDTO:
        # soft delete change the is_active is False
        pass

    @abstractmethod
    def delete_account(self, account_id: str):
        pass

    @abstractmethod
    def get_accounts(self, account_ids: list[str]) -> list[AccountDTO]:
        pass

    @abstractmethod
    def get_user_accounts(self, user_id: str) -> list[AccountDTO]:
        pass

    @abstractmethod
    def validate_account_name_except_current(
            self, name: str, account_id: str) -> bool:
        pass

    @abstractmethod
    def update_account(
            self, account_id: str, field_properties: dict) -> AccountDTO:
        pass

    @abstractmethod
    def is_name_exists(
            self, account_name: str, account_id: Optional[str]) -> bool:
        pass
