import pytest

from task_management.exceptions.enums import ViewType
from task_management.interactors.dtos import CreateViewDTO
from task_management.storages.view_storage import ViewStorage
from task_management.tests.factories.storage_factory import (
    ViewFactory,
    UserFactory
)


class TestViewStorage:

    @pytest.mark.django_db
    def test_get_all_views(self, snapshot):
        # Arrange
        user_id = "12345678-1234-5678-1234-567812345678"
        user = UserFactory(user_id=user_id)
        view_id = "12345678-1234-5678-1234-567812345678"
        view_id2 = "12345678-1234-5678-1234-567812345679"
        ViewFactory(created_by=user, view_id=view_id,
                    view_type=ViewType.TABLE.value)
        ViewFactory(created_by=user, view_id=view_id2,
                    view_type=ViewType.LIST.value)
        storage = ViewStorage()

        # Act
        result = storage.get_all_views()

        # Assert
        snapshot.assert_match(
            repr(result),
            "test_get_all_views.txt"
        )

    @pytest.mark.django_db
    def test_get_view_success(self, snapshot):
        # Arrange
        view_id = "12345678-1234-5678-1234-567812345678"
        user_id = "12345678-1234-5678-1234-567812345678"
        user = UserFactory(user_id=user_id)
        ViewFactory(
            view_id=view_id,
            created_by=user,
            name="Table View"
        )
        storage = ViewStorage()

        # Act
        result = storage.get_view(view_id=str(view_id))

        # Assert
        snapshot.assert_match(
            repr(result),
            "test_get_view_success.txt"
        )

    @pytest.mark.django_db
    def test_create_view(self, snapshot):
        # Arrange
        user_id = "12345678-1234-5678-1234-567812345679"
        UserFactory(user_id=user_id)

        dto = CreateViewDTO(
            name="Board View",
            description="Kanban board",
            view_type=ViewType.TABLE,
            created_by=str(user_id)
        )
        storage = ViewStorage()

        # Act
        result = storage.create_view(create_view_data=dto)

        # Assert
        snapshot.assert_match(
            repr(
                {
                    "name": result.name,
                    "description": result.description,
                    "view_type": result.view_type,
                    "created_by": str(result.created_by),
                }
            ),
            "test_create_view.txt"
        )

    @pytest.mark.django_db
    def test_update_view(self, snapshot):
        # Arrange
        view_id = "12345678-1234-5678-1234-567812345678"
        user_id = "12345678-1234-5678-1234-567812345679"
        user = UserFactory(user_id=user_id)
        ViewFactory(
            view_id=view_id,
            created_by=user,
            name="Old View",
            description="Old description"
        )

        name = "Updated View"
        description = "Updated description"

        storage = ViewStorage()

        # Act
        result = storage.update_view(view_id=view_id, name=name,
                                     description=description)

        # Assert
        snapshot.assert_match(
            repr(result),
            "test_update_view.txt"
        )
