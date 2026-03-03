from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import NothingToUpdateView, ViewNotFound
from task_management.interactors.dtos import ViewDTO
from task_management.interactors.storage_interfaces.view_storage_interface import (
    ViewStorageInterface,
)
from task_management.interactors.views.update_view_interactor import (
    UpdateViewInteractor,
)


class TestUpdateViewInteractor:
    def setup_method(self):
        self.view_storage = create_autospec(ViewStorageInterface)
        self.interactor = UpdateViewInteractor(view_storage=self.view_storage)

    def test_update_view_success(self):
        self.view_storage.check_view_exists.return_value = True
        expected_result = ViewDTO(
            view_id="21bba2fa-ac74-4f41-afb7-4f638eb6a71a",
            name="provide",
            description="Cultural subject almost all late guy.",
            view_type="board",
            created_by="6d5cb6c5-3be9-49ef-8265-85fff230709e",
        )
        self.view_storage.update_view.return_value = expected_result

        result = self.interactor.update_view(
            view_id="view_1",
            name="provide",
            description="Cultural subject almost all late guy.",
        )

        assert result == expected_result

    def test_update_nonexistent_view_raises_exception(self):
        self.view_storage.check_view_exists.return_value = False

        with pytest.raises(ViewNotFound):
            self.interactor.update_view(
                view_id="view_404",
                name="start",
                description="A article detail send task adult.",
            )

    def test_update_view_without_fields_raises_exception(self):
        with pytest.raises(NothingToUpdateView):
            self.interactor.update_view(
                view_id="view_1",
                name=None,
                description=None,
            )
