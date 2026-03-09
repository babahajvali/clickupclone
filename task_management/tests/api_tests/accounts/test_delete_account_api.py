from types import SimpleNamespace

import pytest

from task_management.tests.api_tests.accounts import BaseDeleteAccount


def get_account_data_mock(mocker):
    return mocker.patch(
        'task_management.storages.account_storage.AccountStorage.get_account'
    )


def delete_account_data_mock(mocker):
    return mocker.patch(
        'task_management.storages.account_storage.AccountStorage.delete_account'
    )


def create_account_object(owner_id, is_active=True):
    return type('Account', (),
                {'owner_id': owner_id, 'is_active': is_active})()


@pytest.mark.django_db
class TestDeleteAccountAPI(BaseDeleteAccount):

    def test_delete_account_successfully(self, snapshot, mocker):
        account_id = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'
        owner_id = '49bb508e-c6d1-4882-95fd-1991d103f7dd'

        get_account_mock = get_account_data_mock(mocker=mocker)
        get_account_mock.return_value = create_account_object(
            owner_id=owner_id)

        delete_mock = delete_account_data_mock(mocker=mocker)
        delete_mock.return_value = type(
            'DeletedAccount',
            (),
            {
                'account_id': account_id,
                'name': 'Clickup Clone',
                'description': 'Account deleted',
                'owner_id': owner_id,
                'is_active': False,
            }
        )()

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

    def test_delete_account_with_not_found(self, snapshot, mocker):
        account_id = '49bb508e-c6d1-4882-95fd-1991d103f7de'
        owner_id = '49bb508e-c6d1-4882-95fd-1991d103f7dd'

        get_account_mock = get_account_data_mock(mocker=mocker)
        get_account_mock.return_value = None

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

    def test_delete_account_with_non_owner(self, snapshot, mocker):
        account_id = '49bb508e-c6d1-4882-95fd-1991d103f7de'
        owner_id = '11111111-1111-1111-1111-111111111111'
        other_user_id = '49bb508e-c6d1-4882-95fd-1991d103f7dd'

        get_account_mock = get_account_data_mock(mocker=mocker)
        get_account_mock.return_value = create_account_object(
            owner_id=owner_id)

        variables = {
            'params': {
                'accountId': account_id,
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id=other_user_id),
        )
