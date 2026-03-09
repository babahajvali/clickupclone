from typing import Optional, List

from task_management.interactors.dtos import AccountDTO
from task_management.interactors.storage_interfaces import \
    AccountStorageInterface
from task_management.models import Account


class AccountStorage(AccountStorageInterface):

    @staticmethod
    def _convert_to_account_dto(account_db_object: Account) -> AccountDTO:

        return AccountDTO(
            account_id=account_db_object.account_id,
            name=account_db_object.name,
            description=account_db_object.description,
            owner_id=account_db_object.owner.user_id if account_db_object.owner else None,
            is_active=account_db_object.is_active,
        )

    def get_account(self, account_id: str) -> AccountDTO | None:

        account_data = Account.objects.filter(account_id=account_id).first()

        if not account_data:
            return None

        return self._convert_to_account_dto(account_db_object=account_data)

    def create_account(
            self, name: str, description: Optional[str],
            created_by: str) -> AccountDTO:

        account_data = Account.objects.create(
            name=name, description=description, owner_id=created_by)

        return self._convert_to_account_dto(account_db_object=account_data)

    def delete_account(self, account_id: str) -> AccountDTO:
        Account.objects.filter(account_id=account_id).update(is_active=False)
        return self.get_account(account_id=account_id)

    def get_accounts(self, account_ids: List[str]) -> List[AccountDTO]:
        accounts_data = Account.objects.filter(account_id__in=account_ids)

        return [self._convert_to_account_dto(account_db_object=account_data)
                for account_data in accounts_data]

    def get_existing_account_ids(self, account_ids: List[str]) -> List[str]:
        accounts_ids = Account.objects.filter(
            account_id__in=account_ids).values_list(
            'account_id', flat=True)

        return list(accounts_ids)

    def update_account(
            self, account_id: str, name: Optional[str],
            description: Optional[str]) -> AccountDTO:
        account_properties = {}

        is_name_provided = name is not None
        if is_name_provided:
            account_properties['name'] = name

        is_description_provided = description is not None
        if is_description_provided:
            account_properties['description'] = description

        Account.objects.filter(account_id=account_id).update(
            **account_properties)

        return self.get_account(account_id=account_id)

    def is_account_name_exists(
            self, account_name: str,
            excluded_account_ids: Optional[List[str]]) -> bool:
        account_data = Account.objects.filter(name=account_name)

        if excluded_account_ids:
            account_data = account_data.exclude(
                account_id__in=excluded_account_ids)

        return account_data.exists()
