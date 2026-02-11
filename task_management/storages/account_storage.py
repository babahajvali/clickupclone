from typing import Optional

from django.core.exceptions import ObjectDoesNotExist

from task_management.interactors.dtos import AccountDTO, UpdateAccountDTO
from task_management.interactors.storage_interfaces.account_storage_interface import \
    AccountStorageInterface
from task_management.models import Account, User


class AccountStorage(AccountStorageInterface):

    def get_account_by_id(self, account_id: str) -> AccountDTO | None:
        try:
            account_data = Account.objects.get(account_id=account_id)
            return AccountDTO(
                account_id=account_data.account_id,
                name=account_data.name,
                description=account_data.description,
                owner_id=account_data.owner.user_id,
                is_active=account_data.is_active,
            )
        except ObjectDoesNotExist:
            return None

    def validate_account_name_exists(self, name: str) -> bool:
        return Account.objects.filter(name=name).exists()

    def create_account(self, name: str, description: Optional[str],
                       created_by: str) -> AccountDTO:

        owner = User.objects.get(user_id=created_by)
        account_data = Account.objects.create(name=name,
                                              description=description,
                                              owner=owner)
        return AccountDTO(
            account_id=account_data.account_id,
            name=account_data.name,
            description=account_data.description,
            owner_id=account_data.owner.user_id,
            is_active=account_data.is_active,
        )

    def deactivate_account(self, account_id: str) -> AccountDTO:
        account_data = Account.objects.get(account_id=account_id)
        account_data.is_active = False
        account_data.save()

        return AccountDTO(
            account_id=account_data.account_id,
            name=account_data.name,
            description=account_data.description,
            owner_id=account_data.owner.user_id,
            is_active=account_data.is_active,
        )

    def delete_account(self, account_id: str):
        return Account.objects.get(account_id=account_id).delete()

    def get_accounts(self, account_ids: list[str]) -> list[AccountDTO]:
        accounts_data = Account.objects.filter(account_id__in=account_ids)

        return [AccountDTO(
            account_id=account_data.account_id,
            name=account_data.name,
            description=account_data.description,
            owner_id=account_data.owner.user_id,
            is_active=account_data.is_active,
        ) for account_data in accounts_data]

    def get_user_accounts(self, user_id: str) -> list[AccountDTO]:
        accounts_data = Account.objects.filter(owner_id=user_id,
                                               is_active=True)

        return [AccountDTO(
            account_id=account_data.account_id,
            name=account_data.name,
            description=account_data.description,
            owner_id=account_data.owner.user_id,
            is_active=account_data.is_active,
        ) for account_data in accounts_data]

    def validate_account_name_except_current(self, name: str,
                                             account_id: str) -> bool:
        return Account.objects.filter(name=name).exclude(
            account_id=account_id).exists()

    def update_account(self, account_id: str, update_fields: dict) -> AccountDTO:
        Account.objects.filter(account_id=account_id).update(**update_fields)
        account_data = Account.objects.get(account_id=account_id)

        account_data.save(update_fields=[])

        return AccountDTO(
            account_id=account_data.account_id,
            name=account_data.name,
            description=account_data.description,
            owner_id=account_data.owner.user_id,
            is_active=account_data.is_active,
        )
