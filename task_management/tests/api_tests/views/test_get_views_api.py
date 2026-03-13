from types import SimpleNamespace

import pytest

from task_management.exceptions.enums import ViewType
from task_management.interactors.dtos import ViewDTO
from task_management.tests.api_tests.views import BaseGetViews


def get_all_views_mock(mocker):
    return mocker.patch(
        "task_management.storages.view_storage.ViewStorage.get_all_views"
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
class TestGetViewsAPI(BaseGetViews):
    def test_get_views_successfully(self, snapshot, mocker):
        get_all_views_mock(mocker).return_value = [make_view_dto()]

        self.execute_schema(
            query=self.QUERY,
            variables={},
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )
