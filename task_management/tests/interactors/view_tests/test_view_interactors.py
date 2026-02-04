import pytest
from unittest.mock import create_autospec

from task_management.exceptions.enums import Permissions, ViewType
from task_management.interactors.view_interactors.view_interactors import \
    ViewInteractor
from task_management.interactors.storage_interface.view_storage_interface import \
    ViewStorageInterface
from task_management.interactors.storage_interface.space_permission_storage_interface import \
    SpacePermissionStorageInterface
from task_management.interactors.storage_interface.list_storage_interface import \
    ListStorageInterface
from task_management.exceptions.custom_exceptions import (
    ViewNotFoundException,
    ViewTypeNotFoundException
)
from task_management.tests.factories.interactor_factory import (
    CreateViewDTOFactory,
    UpdateViewDTOFactory,
    ViewDTOFactory
)


class TestViewInteractor:

    def setup_method(self):
        self.view_storage = create_autospec(ViewStorageInterface)
        self.permission_storage = create_autospec(
            SpacePermissionStorageInterface)
        self.list_storage = create_autospec(ListStorageInterface)

        self.interactor = ViewInteractor(
            view_storage=self.view_storage,
            permission_storage=self.permission_storage,
            list_storage=self.list_storage
        )

    def test_create_view_success(self, snapshot):
        # Arrange
        create_data = CreateViewDTOFactory()
        create_data.view_type = ViewType.TABLE
        expected_result = ViewDTOFactory()

        self.view_storage.create_view.return_value = expected_result

        # Act
        result = self.interactor.create_view(create_data)

        # Assert
        snapshot.assert_match(repr(result), "create_view_success.txt")
        self.view_storage.create_view.assert_called_once_with(create_data)

    def test_create_view_with_invalid_view_type_raises_exception(self,
                                                                 snapshot):
        # Arrange
        create_data = CreateViewDTOFactory()
        create_data.view_type = type('MockViewType', (),
                                     {'value': 'invalid_type'})()

        # Act & Assert
        with pytest.raises(ViewTypeNotFoundException) as exc:
            self.interactor.create_view(create_data)

        snapshot.assert_match(repr(exc.value), "create_view_invalid_type.txt")

    def test_update_view_success(self, snapshot):
        # Arrange
        update_data = UpdateViewDTOFactory()
        expected_result = ViewDTOFactory()

        self.permission_storage.get_space_permissions.return_value = (
            Permissions.FULL_EDIT.value
        )
        self.view_storage.get_view.return_value = ViewDTOFactory()
        self.view_storage.update_view.return_value = expected_result

        # Act
        result = self.interactor.update_view(update_data)

        # Assert
        snapshot.assert_match(repr(result), "update_view_success.txt")
        self.view_storage.update_view.assert_called_once_with(update_data)

    def test_update_nonexistent_view_raises_exception(self, snapshot):
        # Arrange
        update_data = UpdateViewDTOFactory()
        self.view_storage.get_view.return_value = None

        # Act & Assert
        with pytest.raises(ViewNotFoundException) as exc:
            self.interactor.update_view(update_data)

        snapshot.assert_match(repr(exc.value), "update_view_not_found.txt")

    def test_get_views_success(self, snapshot):
        # Arrange
        expected_views = [ViewDTOFactory() for _ in range(3)]
        self.view_storage.get_all_views.return_value = expected_views

        # Act
        result = self.interactor.get_views()

        # Assert
        snapshot.assert_match(repr(result), "get_views_success.txt")
        self.view_storage.get_all_views.assert_called_once()
