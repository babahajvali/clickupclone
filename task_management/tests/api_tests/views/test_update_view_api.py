from types import SimpleNamespace

import pytest

from task_management.exceptions.enums import ViewType
from task_management.interactors.dtos import ViewDTO
from task_management.tests.api_tests.views import BaseUpdateView

VIEW_ID = "12345678-1234-5678-1234-567812345679"
MISSING_VIEW_ID = "12345678-1234-5678-1234-567812345681"


def check_view_exists_mock(mocker):
    return mocker.patch(
        "task_management.storages.view_storage.ViewStorage.is_view_exists"
    )


def update_view_mock(mocker):
    return mocker.patch(
        "task_management.storages.view_storage.ViewStorage.update_view"
    )


def make_view_dto() -> ViewDTO:
    return ViewDTO(
        view_id=VIEW_ID,
        name="Updated View",
        description="Updated description",
        view_type=ViewType.BOARD,
        created_by="user_1",
    )


@pytest.mark.django_db
class TestUpdateViewAPI(BaseUpdateView):
    def test_update_view_successfully(self, snapshot, mocker):
        check_view_exists_mock(mocker).return_value = True
        update_view_mock(mocker).return_value = make_view_dto()

        self.execute_schema(
            query=self.QUERY,
            variables={
                "params": {
                    "viewId": VIEW_ID,
                    "name": "Updated View",
                    "description": "Updated description",
                }
            },
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_update_view_not_found(self, snapshot, mocker):
        check_view_exists_mock(mocker).return_value = False

        self.execute_schema(
            query=self.QUERY,
            variables={
                "params": {
                    "viewId": MISSING_VIEW_ID,
                    "name": "Updated View",
                    "description": "Updated description",
                }
            },
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_update_view_nothing_to_update(self, snapshot, mocker):
        self.execute_schema(
            query=self.QUERY,
            variables={
                "params": {
                    "viewId": VIEW_ID,
                    "name": None,
                    "description": None,
                }
            },
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )
