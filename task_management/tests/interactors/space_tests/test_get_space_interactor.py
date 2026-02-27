from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import SpaceNotFound
from task_management.interactors.dtos import SpaceDTO
from task_management.interactors.spaces.get_space_interactor import GetSpaceInteractor
from task_management.interactors.storage_interfaces import SpaceStorageInterface


def make_space(order: int = 1) -> SpaceDTO:
    return SpaceDTO(
        space_id="space_1",
        name="Space",
        description="Desc",
        workspace_id="workspace_1",
        order=order,
        is_deleted=False,
        is_private=False,
        created_by="user_1",
    )


class TestGetSpaceInteractor:
    def setup_method(self):
        self.space_storage = create_autospec(SpaceStorageInterface)
        self.interactor = GetSpaceInteractor(space_storage=self.space_storage)

    def test_get_space_success(self, snapshot):
        self.space_storage.get_space.return_value = make_space()

        result = self.interactor.get_space(space_id="space_1")

        snapshot.assert_match(repr(result), "get_space_success.txt")

    def test_get_space_not_found(self, snapshot):
        self.space_storage.get_space.return_value = None

        with pytest.raises(SpaceNotFound) as exc:
            self.interactor.get_space(space_id="space_1")

        snapshot.assert_match(repr(exc.value), "get_space_not_found.txt")
