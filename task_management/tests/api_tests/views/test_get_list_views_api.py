from types import SimpleNamespace

import pytest

from task_management.exceptions.enums import ViewType
from task_management.interactors.dtos import ListViewDTO
from task_management.tests.api_tests.views import BaseGetListViews

LIST_ID = "12345678-1234-5678-1234-567812345678"
MISSING_LIST_ID = "12345678-1234-5678-1234-567812345680"


def get_list_mock(mocker):
    return mocker.patch(
        "task_management.storages.list_storage.ListStorage.get_list"
    )


def get_list_views_mock(mocker):
    return mocker.patch(
        "task_management.storages.list_view_storage.ListViewStorage.get_list_views"
    )


def make_list_view_dto() -> ListViewDTO:
    return ListViewDTO(
        id=1,
        view_name="Table",
        list_id=LIST_ID,
        view_type=ViewType.TABLE,
        created_by="user_1",
        is_active=True,
    )


@pytest.mark.django_db
class TestGetListViewsAPI(BaseGetListViews):
    def test_get_list_views_successfully(self, snapshot, mocker):
        get_list_mock(mocker).return_value = type(
            "List", (), {"is_deleted": False}
        )()
        get_list_views_mock(mocker).return_value = [make_list_view_dto()]

        self.execute_schema(
            query=self.QUERY,
            variables={"params": {"listId": LIST_ID}},
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_get_list_views_list_not_found(self, snapshot, mocker):
        get_list_mock(mocker).return_value = None

        self.execute_schema(
            query=self.QUERY,
            variables={"params": {"listId": MISSING_LIST_ID}},
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_get_list_views_deleted_list(self, snapshot, mocker):
        get_list_mock(mocker).return_value = type(
            "List", (), {"is_deleted": True}
        )()

        self.execute_schema(
            query=self.QUERY,
            variables={"params": {"listId": LIST_ID}},
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )
