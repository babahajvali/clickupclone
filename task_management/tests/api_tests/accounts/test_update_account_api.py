from types import SimpleNamespace

import pytest

from task_management.tests.api_tests.accounts import BaseUpdateAccount
from task_management.tests.factories.api_factory import AccountDTOFactory


def get_account_data_mock(mocker):
    return mocker.patch(
        'task_management.storages.account_storage.AccountStorage.get_account'
    )


def is_account_name_exists_mock(mocker):
    return mocker.patch(
        'task_management.storages.account_storage.AccountStorage.is_account_name_exists'
    )


def update_account_data_mock(mocker):
    return mocker.patch(
        'task_management.storages.account_storage.AccountStorage.update_account'
    )


def create_account_object(owner_id, is_active=True):
    return type('Account', (),
                {'owner_id': owner_id, 'is_active': is_active})()


@pytest.mark.django_db
class TestUpdateAccountAPI(BaseUpdateAccount):

    def test_update_account_successfully(self, snapshot, mocker):
        account_id = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'
        owner_id = '49bb508e-c6d1-4882-95fd-1991d103f7dd'

        get_account_mock = get_account_data_mock(mocker=mocker)
        get_account_mock.return_value = create_account_object(
            owner_id=owner_id)

        name_exists_mock = is_account_name_exists_mock(mocker=mocker)
        name_exists_mock.return_value = False

        update_mock = update_account_data_mock(mocker=mocker)
        update_mock.return_value = AccountDTOFactory(
            account_id=account_id,
            name='Clickup Clone Updated',
            description='Updated account description',
            owner_id=owner_id,
            is_active=True,
        )

        variables = {
            'params': {
                'accountId': account_id,
                'name': 'Clickup Clone Updated',
                'description': 'Updated account description',
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id=owner_id),
        )

    def test_update_account_with_not_found(self, snapshot, mocker):
        account_id = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'
        owner_id = '49bb508e-c6d1-4882-95fd-1991d103f7dd'

        get_account_mock = get_account_data_mock(mocker=mocker)
        get_account_mock.return_value = None

        name_exists_mock = is_account_name_exists_mock(mocker=mocker)
        name_exists_mock.return_value = False

        variables = {
            'params': {
                'accountId': account_id,
                'name': 'Clickup Clone Updated',
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id=owner_id),
        )

    def test_update_account_with_inactive_account(self, snapshot, mocker):
        account_id = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'
        owner_id = '49bb508e-c6d1-4882-95fd-1991d103f7dd'

        get_account_mock = get_account_data_mock(mocker=mocker)
        get_account_mock.return_value = create_account_object(
            owner_id=owner_id, is_active=False)

        name_exists_mock = is_account_name_exists_mock(mocker=mocker)
        name_exists_mock.return_value = False

        variables = {
            'params': {
                'accountId': account_id,
                'name': 'Clickup Clone Updated',
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id=owner_id),
        )

    def test_update_account_with_non_owner(self, snapshot, mocker):
        account_id = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'
        owner_id = '11111111-1111-1111-1111-111111111111'
        other_user_id = '49bb508e-c6d1-4882-95fd-1991d103f7dd'

        get_account_mock = get_account_data_mock(mocker=mocker)
        get_account_mock.return_value = create_account_object(
            owner_id=owner_id)

        variables = {
            'params': {
                'accountId': account_id,
                'description': 'Updated accounts description',
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id=other_user_id),
        )

    def test_update_account_with_duplicate_name(self, snapshot, mocker):
        account_id = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'
        owner_id = '49bb508e-c6d1-4882-95fd-1991d103f7dd'

        get_account_mock = get_account_data_mock(mocker=mocker)
        get_account_mock.return_value = create_account_object(
            owner_id=owner_id)

        name_exists_mock = is_account_name_exists_mock(mocker=mocker)
        name_exists_mock.return_value = True

        variables = {
            'params': {
                'accountId': account_id,
                'name': 'Clickup Clone Updated',
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id=owner_id),
        )

    def test_update_account_with_nothing_to_update(self, snapshot):
        account_id = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'
        owner_id = '49bb508e-c6d1-4882-95fd-1991d103f7dd'

        variables = {
            'params': {
                'accountId': account_id,
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id=owner_id),
        )

    def test_update_account_with_empty_name(self, snapshot):
        account_id = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'
        owner_id = '49bb508e-c6d1-4882-95fd-1991d103f7dd'

        variables = {
            'params': {
                'accountId': account_id,
                'name': '',
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id=owner_id),
        )
