import pytest

from task_management.tests.api_tests.account import BaseCreateAccount
from task_management.tests.factories.api_factory import AccountDTOFactory, \
    UserDTOFactory
from task_management.tests.factories.storage_factory import UserFactory, \
    ViewFactory


def get_list_view_id_mock(mocker):
    return mocker.patch(
        'task_management.storages.view_storage.ViewStorage.get_list_view_id'
    )


def get_user_data_mock(mocker):
    return mocker.patch(
        'task_management.storages.user_storage.UserStorage.get_user'
    )


def get_create_account_mock(mocker):
    return mocker.patch(
        'task_management.storages.account_storage.AccountStorage.create_account'
    )


@pytest.mark.django_db
class TestCreateAccountAPI(BaseCreateAccount):

    def test_create_account_successfully(self, snapshot, mocker):
        # Arrange
        user_id = "49bb508e-c6d1-4882-95fd-1991d103f7dd"
        fixed_account_id = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"

        UserFactory(user_id=user_id, is_active=True)
        view = ViewFactory(created_by_id=user_id)
        list_view_mock = get_list_view_id_mock(mocker=mocker)
        list_view_mock.return_value = str(view.view_id)

        account_mock = get_create_account_mock(mocker=mocker)
        account_mock.return_value = AccountDTOFactory(
            account_id=fixed_account_id)

        variables = {
            "params": {
                "name": "Clickup Clone 1",
                "description": "This is first company",
                "ownerId": user_id
            }
        }
        # Act
        result = self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
        )

        print(result)

    def test_create_account_with_empty_name(self, snapshot, mocker):
        # Arrange
        user_mock = get_user_data_mock(mocker=mocker)
        user_mock.return_value = UserDTOFactory(
            user_id="49bb508e-c6d1-4882-95fd-1991d103f7dd",
            is_active=True
        )
        variables = {
            "params": {
                "name": "",
                "description": "This is first company",
                "ownerId": "49bb508e-c6d1-4882-95fd-1991d103f7dd"
            }
        }
        # Act
        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
        )

    def test_create_account_with_inactive_user(self, snapshot, mocker):
        # Arrange
        user_mock = get_user_data_mock(mocker=mocker)
        user_mock.return_value = UserDTOFactory(
            user_id="49bb508e-c6d1-4882-95fd-1991d103f7dd",
            is_active=False
        )
        variables = {
            "params": {
                "name": "Clickup Clone 1",
                "description": "This is first company",
                "ownerId": "49bb508e-c6d1-4882-95fd-1991d103f7dd"
            }
        }
        # Act
        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
        )

    def test_create_account_with_user_not_found(self, snapshot, mocker):
        # Arrange
        user_mock = get_user_data_mock(mocker=mocker)
        user_mock.return_value = None
        variables = {
            "params": {
                "name": "Clickup Clone 1",
                "description": "This is first company",
                "ownerId": "49bb508e-c6d1-4882-95fd-1991d103f7dd"
            }
        }
        # Act
        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
        )

    def test_create_account_with_duplicate_name(self, snapshot, mocker):
        # Arrange
        AccountDTOFactory.create(name="Clickup Clone 1")
        user_mock = get_user_data_mock(mocker=mocker)
        user_mock.return_value = UserDTOFactory(
            user_id="49bb508e-c6d1-4882-95fd-1991d103f7dd",
            is_active=True
        )
        variables = {
            "params": {
                "name": "Clickup Clone 1",
                "description": "This is first company",
                "ownerId": "49bb508e-c6d1-4882-95fd-1991d103f7dd"
            }
        }
        # Act
        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
        )
