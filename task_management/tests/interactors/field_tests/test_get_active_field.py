from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import FieldNotFound
from task_management.exceptions.enums import FieldType
from task_management.interactors.dtos import FieldDTO
from task_management.interactors.fields.get_field_interactor import \
    GetFieldInteractor
from task_management.interactors.storage_interfaces import (
    FieldStorageInterface
)


class TestGetActiveFieldInteractor:
    @staticmethod
    def _get_field_dto():
        return FieldDTO(
            field_id="field_1",
            field_type=FieldType.TEXT,
            description="Task priority",
            template_id="tpl_1",
            field_name="Priority",
            order=1,
            is_deleted=False,
            config={"max_length": 10},
            is_required=True,
            created_by="user_1",
        )

    def setup_method(self):
        self.field_storage = create_autospec(FieldStorageInterface)

        self.interactor = GetFieldInteractor(
            field_storage=self.field_storage
        )

    def _setup_get_field_dependencies(self, *,
                                      field_data: FieldDTO | None = None):
        if field_data is None:
            field_data = self._get_field_dto()

        self.field_storage.get_field.return_value = field_data

    def test_get_active_field_success(self, snapshot):
        # Arrange
        self._setup_get_field_dependencies()

        # Act
        result = self.interactor.get_field(field_id="field_1")

        snapshot.assert_match(
            repr(result),
            "test_get_active_field_success.txt",
        )

    def test_get_active_field_not_found(self, snapshot):
        # Arrange
        self._setup_get_field_dependencies(field_data=None)
        self.field_storage.get_field.return_value = None

        # Act
        with pytest.raises(FieldNotFound) as exc:
            self.interactor.get_field(field_id="field_1")

        snapshot.assert_match(
            repr(exc.value.field_id),
            "test_get_active_field_not_found.txt",
        )
