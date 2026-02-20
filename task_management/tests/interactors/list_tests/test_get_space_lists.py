import pytest
from unittest.mock import create_autospec, patch

from task_management.interactors.list.list_interactor import \
    ListInteractor
from task_management.exceptions.custom_exceptions import (
    SpaceNotFoundException,
    InactiveSpaceException,
)
from task_management.interactors.storage_interfaces import \
    ListStorageInterface, FolderStorageInterface, SpaceStorageInterface, \
    WorkspaceStorageInterface



class TestGetSpaceLists:

    def setup_method(self):
        self.list_storage = create_autospec(ListStorageInterface)
        self.folder_storage = create_autospec(FolderStorageInterface)
        self.space_storage = create_autospec(SpaceStorageInterface)
        self.workspace_storage = create_autospec(WorkspaceStorageInterface)

        self.interactor = ListInteractor(
            list_storage=self.list_storage,
            folder_storage=self.folder_storage,
            space_storage=self.space_storage,
            workspace_storage=self.workspace_storage
        )

    def test_get_space_lists_success(self, snapshot):
        self.interactor.space_storage.get_space.return_value = type(
            "Space", (), {"is_active": True}
        )()
        self.interactor.list_storage.get_active_space_lists.return_value = ["LIST1"]

        result = self.interactor.get_active_space_lists("space_1")

        snapshot.assert_match(repr(result), "get_space_lists_success.json")

    def test_space_not_found(self, snapshot):
        with patch("django.core.cache.cache.get", return_value=None):
            self.interactor.space_storage.get_space.return_value = None

            with pytest.raises(SpaceNotFoundException) as exc:
                self.interactor.get_active_space_lists("space_1")

        snapshot.assert_match(repr(exc.value), "space_not_found.txt")

    def test_space_inactive(self, snapshot):
        with patch("django.core.cache.cache.get", return_value=None):
            self.interactor.space_storage.get_space.return_value = type(
                "Space", (), {"is_active": False}
            )()

            with pytest.raises(InactiveSpaceException) as exc:
                self.interactor.get_active_space_lists("space_1")

        snapshot.assert_match(repr(exc.value), "space_inactive.txt")
