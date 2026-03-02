import pytest
from unittest.mock import create_autospec

from task_management.exceptions.enums import ViewTypes
from task_management.interactors.views.view_interactor import \
    ViewInteractor
from task_management.interactors.storage_interfaces.view_storage_interface import \
    ViewStorageInterface
from task_management.interactors.storage_interfaces.list_storage_interface import \
    ListStorageInterface
from task_management.exceptions.custom_exceptions import (
    ViewNotFound,
    ViewTypeNotFound
)
from task_management.interactors.dtos import CreateViewDTO, ViewDTO


class TestViewInteractor:

    def setup_method(self):
        self.view_storage = create_autospec(ViewStorageInterface)

        self.list_storage = create_autospec(ListStorageInterface)

        self.interactor = ViewInteractor(
            view_storage=self.view_storage,
            list_storage=self.list_storage
        )

    def test_create_view_success(self, snapshot):
        # Arrange
        create_data = CreateViewDTO(
            name="be",
            description="Raise study modern miss dog Democrat quickly.",
            view_type=ViewTypes.LIST,
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

        # Act
        result = self.interactor.create_view(create_data)

        # Assert
        snapshot.assert_match(repr(result), "create_view_success.txt")
        self.view_storage.create_view.assert_called_once_with(create_data)

    def test_create_view_with_invalid_view_type_raises_exception(self,
                                                                 snapshot):
        # Arrange
        create_data = CreateViewDTO(
            name="name",
            description="description",
            view_type=type("MockViewType", (), {"value": "invalid_type"})(),
            created_by="user_1",
        )

        # Act & Assert
        with pytest.raises(ViewTypeNotFound) as exc:
            self.interactor.create_view(create_data)

        snapshot.assert_match(repr(exc.value), "create_view_invalid_type.txt")

    def test_update_view_success(self, snapshot):
        # Arrange
        update_data = type(
            "UpdateDTO",
            (),
            {"view_id": "view_1", "name": "provide",
             "description": "Cultural subject almost all late guy."},
        )()
        expected_result = ViewDTO(
            view_id="21bba2fa-ac74-4f41-afb7-4f638eb6a71a",
            name="provide",
            description="Cultural subject almost all late guy.",
            view_type="board",
            created_by="6d5cb6c5-3be9-49ef-8265-85fff230709e",
        )

        self.view_storage.check_view_exists.return_value = True
        self.view_storage.update_view.return_value = expected_result

        # Act
        result = self.interactor.update_view(
            view_id=update_data.view_id, name=update_data.name,
            description=update_data.description)

        # Assert
        snapshot.assert_match(repr(result), "update_view_success.txt")

    def test_update_nonexistent_view_raises_exception(self, snapshot):
        # Arrange
        update_data = type(
            "UpdateDTO",
            (),
            {"view_id": "view_404", "name": "start",
             "description": "A article detail send task adult."},
        )()
        self.view_storage.check_view_exists.return_value = False

        # Act & Assert
        with pytest.raises(ViewNotFound) as exc:
            self.interactor.update_view(
                view_id=update_data.view_id, name=update_data.name,
                description=update_data.description)

        snapshot.assert_match(repr(exc.value), "update_view_not_found.txt")

    def test_get_views_success(self, snapshot):
        # Arrange
        expected_views = [
            ViewDTO(
                view_id="126cbc8f-3888-4479-91eb-cd49428a1c22",
                name="radio",
                description="Go Congress mean always beyond.",
                view_type="table",
                created_by="429817c5-3308-4b2e-a42a-ad48fcfcfa81",
            ),
            ViewDTO(
                view_id="78601602-bb4a-46cb-a786-ab375bca47be",
                name="this",
                description="College pull whom around put suddenly garden.",
                view_type="lists",
                created_by="ebe21368-98c7-4205-9e01-a934402d0baf",
            ),
            ViewDTO(
                view_id="0361524c-2cc0-4859-aa65-24ab713b7e05",
                name="market",
                description="Tonight themselves true power home price.",
                view_type="board",
                created_by="032f06ca-b0d9-42aa-8f83-7ef727460f22",
            ),
        ]
        self.view_storage.get_all_views.return_value = expected_views

        # Act
        result = self.interactor.get_all_views()

        # Assert
        snapshot.assert_match(repr(result), "get_views_success.txt")
        self.view_storage.get_all_views.assert_called_once()
