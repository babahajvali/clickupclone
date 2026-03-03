from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import DeletedListFound, ListNotFound
from task_management.interactors.dtos import ListViewDTO
from task_management.interactors.storage_interfaces.list_storage_interface import (
    ListStorageInterface,
)
from task_management.interactors.storage_interfaces.view_storage_interface import (
    ViewStorageInterface,
)
from task_management.interactors.views.get_list_views_interactor import (
    GetListViewsInteractor,
)


class TestGetListViewsInteractor:
    def setup_method(self):
        self.list_storage = create_autospec(ListStorageInterface)
        self.view_storage = create_autospec(ViewStorageInterface)
        self.interactor = GetListViewsInteractor(
            list_storage=self.list_storage,
            view_storage=self.view_storage,
        )

    def test_get_list_views_success(self):
        self.list_storage.get_list.return_value = type(
            "List", (), {"is_deleted": False}
        )()
        expected = [
            ListViewDTO(
                id=2,
                list_id="list_1",
                view_id="view_1",
                applied_by="user_1",
                is_active=True,
            ),
            ListViewDTO(
                id=3,
                list_id="list_1",
                view_id="view_2",
                applied_by="user_2",
                is_active=True,
            ),
        ]
        self.view_storage.get_list_views.return_value = expected

        result = self.interactor.get_list_views("list_id")

        assert result == expected

    def test_get_views_for_inactive_list_raises_exception(self):
        self.list_storage.get_list.return_value = type(
            "List", (), {"is_deleted": True}
        )()

        with pytest.raises(DeletedListFound):
            self.interactor.get_list_views("list_id")

    def test_get_views_for_nonexistent_list_raises_exception(self):
        self.list_storage.get_list.return_value = None

        with pytest.raises(ListNotFound):
            self.interactor.get_list_views("list_id")
