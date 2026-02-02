from task_management.interactors.dtos import AccountDTO, CreateAccountDTO
from task_management.interactors.storage_interface.account_storage_interface import \
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
        except Account.DoesNotExist:
            return None

    def validate_account_name_exists(self, name: str) -> bool:
        return Account.objects.filter(name=name).exists()

    def create_account(self, account_dto: CreateAccountDTO) -> AccountDTO:

        owner = User.objects.get(user_id=account_dto.owner_id)
        account_data = Account.objects.create(name=account_dto.name, description=account_dto.description,owner=owner)
        return AccountDTO(
            account_id=account_data.account_id,
            name=account_data.name,
            description=account_data.description,
            owner_id=account_data.owner.user_id,
            is_active=account_data.is_active,
        )

    def transfer_account(self, account_id: str,
                         new_owner_id: str) -> AccountDTO:
        user = User.objects.get(user_id=new_owner_id)
        account_data = Account.objects.get(account_id=account_id)
        account_data.owner = user
        account_data.save()

        return AccountDTO(
            account_id=account_data.account_id,
            name=account_data.name,
            description=account_data.description,
            owner_id=account_data.owner.user_id,
            is_active=account_data.is_active,
        )

    def delete_account(self, account_id: str) -> AccountDTO:
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

    def get_accounts(self,account_ids: list[str]) -> list[AccountDTO]:
        accounts_data =  Account.objects.filter(account_id__in=account_ids,is_active=True)

        return [AccountDTO(
            account_id=account_data.account_id,
            name=account_data.name,
            description=account_data.description,
            owner_id=account_data.owner.user_id,
            is_active=account_data.is_active,
        ) for account_data in accounts_data]
