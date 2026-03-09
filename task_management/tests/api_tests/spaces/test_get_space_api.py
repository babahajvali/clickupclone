import pytest

from task_management.interactors.dtos import SpaceDTO
from task_management.tests.api_tests.spaces import BaseGetSpace


def get_space_mock(mocker):
    return mocker.patch(
        "task_management.storages.space_storage.SpaceStorage.get_space"
    )


def make_space() -> SpaceDTO:
    return SpaceDTO(
        space_id="space_1",
        name="Engineering",
        description="Engineering space",
        workspace_id="workspace_1",
        order=1,
        is_deleted=False,
        is_private=False,
        created_by="user_1",
    )


@pytest.mark.django_db
class TestGetSpaceAPI(BaseGetSpace):
    def test_get_space_successfully(self, snapshot, mocker):
        get_space = get_space_mock(mocker)
        get_space.return_value = make_space()

        variables = {"params": {"spaceId": "space_1"}}

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
        )

    def test_get_space_not_found(self, snapshot, mocker):
        get_space = get_space_mock(mocker)
        get_space.return_value = None

        variables = {"params": {"spaceId": "space_404"}}

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
        )
