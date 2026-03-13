from types import SimpleNamespace

import pytest

from task_management.exceptions.enums import ViewType
from task_management.interactors.dtos import ViewDTO
from task_management.tests.api_tests.views import BaseCreateView


def create_view_mock(mocker):
    return mocker.patch(
        "task_management.storages.view_storage.ViewStorage.create_view"
    )


def make_view_dto() -> ViewDTO:
    return ViewDTO(
        view_id="view_1",
        name="List View",
        description="Main list view",
        view_type=ViewType.LIST,
        created_by="user_1",
    )


@pytest.mark.django_db
class TestCreateViewAPI(BaseCreateView):
    def test_create_view_successfully(self, snapshot, mocker):
        create_view_mock(mocker).return_value = make_view_dto()

        self.execute_schema(
            query=self.QUERY,
            variables={
                "params": {
                    "name": "List View",
                    "description": "Main list view",
                    "viewType": "LIST",
                }
            },
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_create_view_invalid_view_type(self, snapshot, mocker):
        self.execute_schema(
            query=self.QUERY,
            variables={
                "params": {
                    "name": "List View",
                    "description": "Main list view",
                    "viewType": "INVALID",
                }
            },
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_create_view_empty_name(self, snapshot, mocker):
        self.execute_schema(
            query=self.QUERY,
            variables={
                "params": {
                    "name": "   ",
                    "description": "Main list view",
                    "viewType": "LIST",
                }
            },
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )
