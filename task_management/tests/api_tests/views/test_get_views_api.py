from types import SimpleNamespace

import pytest

from task_management.exceptions.enums import ViewType
from task_management.graphql.types.types import ViewsType
from task_management.tests.api_tests.views import BaseGetViews


def get_all_views_mock(mocker):
    return mocker.patch(
        "task_management.graphql.resolvers.view.get_views_resolver.get_all_views_resolver"
    )


@pytest.mark.django_db
class TestGetViewsAPI(BaseGetViews):
    def test_get_views_successfully(self, snapshot, mocker):
        get_all_views_mock(mocker).return_value = ViewsType(views=["TABLE", "CALENDAR", "BOARD"])

        self.execute_schema(
            query=self.QUERY,
            variables={},
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )
