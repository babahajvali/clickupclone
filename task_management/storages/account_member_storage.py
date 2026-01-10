from task_management.exceptions.enums import Role
from task_management.interactors.dtos import AccountMemberDTO, \
    CreateAccountMemberDTO
from task_management.interactors.storage_interface.account_member_storage_interface import \
    AccountMemberStorageInterface
from task_management.models import AccountMember, User, Account


class AccountMemberStorage(AccountMemberStorageInterface):

    @staticmethod
    def _account_member_dto(
            account_member_data: AccountMember) -> AccountMemberDTO:
        return AccountMemberDTO(
            id=account_member_data.pk,
            account_id=account_member_data.account.account_id,
            user_id=account_member_data.user.user_id,
            is_active=account_member_data.is_active,
            role=account_member_data.role,
            added_by=account_member_data.added_by.user_id,
        )

    def get_user_permission_for_account(self, account_id: str,
                                        user_id: str) -> AccountMemberDTO | None:
        try:
            account_member_data = AccountMember.objects.get(account_id=account_id,
                                                            user_id=user_id)

            return self._account_member_dto(
                account_member_data=account_member_data)
        except AccountMember.DoesNotExist:
            return None

    def add_member_to_account(self,
                              user_data: CreateAccountMemberDTO) -> AccountMemberDTO:
        user_ids = [user_data.user_id]
        if user_data.added_by:
            user_ids.append(user_data.added_by)

        users = User.objects.filter(user_id__in=user_ids)
        user_dict = {u.user_id: u for u in users}

        user = user_dict[user_data.user_id]
        added_by = user_dict.get(user_data.added_by)

        account = Account.objects.get(account_id=user_data.account_id)

        account_member_data = AccountMember.objects.create(
            account=account,
            user=user,
            added_by=added_by,
            role=user_data.role.value
        )

        return self._account_member_dto(account_member_data)

    def update_member_role(
            self, account_member_id: int, role: Role) -> AccountMemberDTO:
        account_member_data = AccountMember.objects.get(pk=account_member_id)
        account_member_data.role = role
        account_member_data.save()

        return self._account_member_dto(
            account_member_data=account_member_data)

    def get_account_member_permission(self,
                                      account_member_id: int) -> AccountMemberDTO:
        account_member_data = AccountMember.objects.get(pk=account_member_id)

        return self._account_member_dto(
            account_member_data=account_member_data)

    def delete_account_member_permission(
            self, account_member_id: int) -> AccountMemberDTO:
        account_member_data = AccountMember.objects.get(pk=account_member_id)
        account_member_data.is_active = False
        account_member_data.save()

        return self._account_member_dto(
            account_member_data=account_member_data)
