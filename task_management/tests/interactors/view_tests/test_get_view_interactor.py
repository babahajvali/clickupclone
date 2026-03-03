from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import ViewNotFound
from task_management.interactors.dtos import ViewDTO
from task_management.interactors.storage_interfaces.view_storage_interface import (
    ViewStorageInterface,
)
from task_management.interactors.views.get_view_interactor import GetViewInteractor


class TestGetViewInteractor:
    def setup_method(self):
        self.view_storage = create_autospec(ViewStorageInterface)
        self.interactor = GetViewInteractor(view_storage=self.view_storage)

    def test_get_view_success(self):
        expected = ViewDTO(
            view_id="view_1",
            name="View Name",
            description="View Description",
            view_type="list",
            created_by="user_1",
        )
        self.view_storage.check_view_exists.return_value = True
        self.view_storage.get_view.return_value = expected

        result = self.interactor.get_view(view_id="view_1")

        assert result == expected

    def test_get_view_not_found(self):
        self.view_storage.check_view_exists.return_value = False

        with pytest.raises(ViewNotFound):
            self.interactor.get_view(view_id="view_404")
