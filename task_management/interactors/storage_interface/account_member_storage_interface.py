from abc import ABC, abstractmethod

from task_management.exceptions.enums import Role
from task_management.interactors.dtos import AccountMemberDTO, \
    CreateAccountMemberDTO


class AccountMemberStorageInterface(ABC):

    @abstractmethod
    def get_user_permission_for_account(self, account_id: str,
                                        user_id: str) -> AccountMemberDTO:
        pass

    @abstractmethod
    def add_member_to_account(self, user_data: CreateAccountMemberDTO) -> \
            AccountMemberDTO:
        pass

    @abstractmethod
    def update_member_role(
            self, account_member_id: int, role: Role) -> AccountMemberDTO:
        pass

    @abstractmethod
    def get_account_member_permission(self,
                                      account_member_id: int) -> AccountMemberDTO:
        pass

    @abstractmethod
    def delete_account_member_permission(
            self,account_member_id: int) -> AccountMemberDTO:
        pass
