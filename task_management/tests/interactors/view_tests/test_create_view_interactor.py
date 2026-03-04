from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import ViewTypeNotFound
from task_management.exceptions.enums import ViewType
from task_management.interactors.dtos import CreateViewDTO, ViewDTO
from task_management.interactors.storage_interfaces.view_storage_interface import (
    ViewStorageInterface,
)
from task_management.interactors.views.create_view_interactor import (
    CreateViewInteractor,
)


class TestCreateViewInteractor:
    def setup_method(self):
        self.view_storage = create_autospec(ViewStorageInterface)
        self.interactor = CreateViewInteractor(view_storage=self.view_storage)

    def test_create_view_success(self):
        create_data = CreateViewDTO(
            name="be",
            description="Raise study modern miss dog Democrat quickly.",
            view_type=ViewType.LIST,
            created_by="9466e472-6b5f-4241-b323-ca74d3447490",
        )
        expected_result = ViewDTO(
            view_id="d7ab7928-09e4-49e6-ac62-b2c82648ee38",
            name="be",
            description="Raise study modern miss dog Democrat quickly.",
            view_type="lists",
            created_by="9466e472-6b5f-4241-b323-ca74d3447490",
        )
        self.view_storage.create_view.return_value = expected_result

        result = self.interactor.create_view(create_view_data=create_data)

        assert result == expected_result
        self.view_storage.create_view.assert_called_once_with(create_data)

    def test_create_view_with_invalid_view_type_raises_exception(self):
        create_data = CreateViewDTO(
            name="name",
            description="description",
            view_type=type("MockViewType", (), {"value": "invalid_type"})(),
            created_by="user_1",
        )

        with pytest.raises(ViewTypeNotFound):
            self.interactor.create_view(create_view_data=create_data)
