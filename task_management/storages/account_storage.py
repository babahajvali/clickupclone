from typing import Optional, List

from django.core.exceptions import ObjectDoesNotExist

from task_management.interactors.dtos import AccountDTO
from task_management.interactors.storage_interfaces import \
    AccountStorageInterface

from task_management.models import Account


class AccountStorage(AccountStorageInterface):

    def get_account_by_id(self, account_id: str) -> AccountDTO | None:
        try:
            account_data = Account.objects.get(account_id=account_id)
            return AccountDTO(
                account_id=account_data.account_id,
                name=account_data.name,
                description=account_data.description,
                owner_id=account_data.owner.user_id,
                is_active=account_data.is_delete,
            )
        except ObjectDoesNotExist:
            return None

    def create_account(
            self, name: str, description: Optional[str],
            created_by: str) -> AccountDTO:

        account_data = Account.objects.create(
            name=name, description=description, owner_id=created_by)
        return AccountDTO(
            account_id=account_data.account_id,
            name=account_data.name,
            description=account_data.description,
            owner_id=account_data.owner.user_id,
            is_active=account_data.is_delete,
        )

    def deactivate_account(self, account_id: str) -> AccountDTO:
        account_data = Account.objects.get(account_id=account_id)
        account_data.is_delete = False
        account_data.save()

        return AccountDTO(
            account_id=account_data.account_id,
            name=account_data.name,
            description=account_data.description,
            owner_id=account_data.owner.user_id,
            is_active=account_data.is_delete,
        )

    def delete_account(self, account_id: str):
        return Account.objects.get(account_id=account_id).delete()

    def get_accounts(self, account_ids: List[str]) -> List[AccountDTO]:
        accounts_data = Account.objects.filter(account_id__in=account_ids)

        return [AccountDTO(
            account_id=account_data.account_id,
            name=account_data.name,
            description=account_data.description,
            owner_id=account_data.owner.user_id,
            is_active=account_data.is_delete,
        ) for account_data in accounts_data]

    def get_existing_account_ids(self, account_ids: List[str]) -> List[str]:
        accounts_ids = Account.objects.filter(
            account_id__in=account_ids).values('account_id')

        return [str(each['account_id']) for each in accounts_ids]

    def get_user_accounts(self, user_id: str) -> List[AccountDTO]:
        accounts_data = Account.objects.filter(
            owner_id=user_id, is_active=True)

        return [AccountDTO(
            account_id=account_data.account_id,
            name=account_data.name,
            description=account_data.description,
            owner_id=account_data.owner.user_id,
            is_active=account_data.is_delete,
        ) for account_data in accounts_data]

    def update_account(
            self, account_id: str, name: Optional[str],
            description: Optional[str]) -> AccountDTO:
        field_properties = {}

        is_name_provided = name is not None
        if is_name_provided:
            field_properties['name'] = name

        is_description_provided = description is not None
        if is_description_provided:
            field_properties['description'] = description

        Account.objects.filter(account_id=account_id).update(
            **field_properties)
        account_data = Account.objects.get(account_id=account_id)

        return AccountDTO(
            account_id=account_data.account_id,
            name=account_data.name,
            description=account_data.description,
            owner_id=account_data.owner.user_id,
            is_active=account_data.is_delete,
        )

    def is_account_name_exists(
            self, account_name: str, account_id: Optional[str]) -> bool:
        account_data = Account.objects.filter(name=account_name)

        if account_id:
            account_data = account_data.exclude(account_id=account_id)

        return account_data.exists()
