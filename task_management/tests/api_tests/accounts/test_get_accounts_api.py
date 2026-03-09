import pytest

from task_management.tests.api_tests.accounts import BaseGetAccounts
from task_management.tests.factories.api_factory import AccountDTOFactory


def get_existing_account_ids_mock(mocker):
    return mocker.patch(
        'task_management.storages.account_storage.AccountStorage.get_existing_account_ids'
    )


def get_accounts_data_mock(mocker):
    return mocker.patch(
        'task_management.storages.account_storage.AccountStorage.get_accounts'
    )


@pytest.mark.django_db
class TestGetAccountsAPI(BaseGetAccounts):

    def test_get_accounts_successfully(self, snapshot, mocker):
        account_id_1 = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'
        account_id_2 = 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb'

        existing_ids_mock = get_existing_account_ids_mock(mocker=mocker)
        existing_ids_mock.return_value = [account_id_1, account_id_2]

        get_accounts_mock = get_accounts_data_mock(mocker=mocker)
        get_accounts_mock.return_value = [
            AccountDTOFactory(
                account_id=account_id_1,
                name='Clickup Clone 1',
                description='This is first company',
                owner_id='49bb508e-c6d1-4882-95fd-1991d103f7dd',
                is_active=True,
            ),
            AccountDTOFactory(
                account_id=account_id_2,
                name='Clickup Clone 2',
                description='This is second company',
                owner_id='59bb508e-c6d1-4882-95fd-1991d103f7dd',
                is_active=True,
            ),
        ]

        variables = {
            'params': {
                'accountIds': [account_id_1, account_id_2],
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
        )

    def test_get_accounts_with_invalid_account_ids(self, snapshot, mocker):
        valid_account_id = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'
        invalid_account_id = 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb'

        existing_ids_mock = get_existing_account_ids_mock(mocker=mocker)
        existing_ids_mock.return_value = [valid_account_id]

        variables = {
            'params': {
                'accountIds': [valid_account_id, invalid_account_id],
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
        )

    def test_get_accounts_with_empty_account_ids(self, snapshot, mocker):
        existing_ids_mock = get_existing_account_ids_mock(mocker=mocker)
        existing_ids_mock.return_value = []

        get_accounts_mock = get_accounts_data_mock(mocker=mocker)
        get_accounts_mock.return_value = []

        variables = {
            'params': {
                'accountIds': [],
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
        )
