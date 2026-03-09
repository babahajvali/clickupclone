from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import InvalidFieldIdsFound
from task_management.exceptions.enums import FieldType
from task_management.interactors.dtos import FieldDTO
from task_management.interactors.fields.get_fields_interactor import \
    GetFieldsInteractor
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

        self.interactor = GetFieldsInteractor(
            field_storage=self.field_storage
        )

    def _setup_get_field_dependencies(self, *,
                                      field_data: FieldDTO | None = None,
                                      existing_field_ids: list[str] | None = None):
        if field_data is None:
            field_data = self._get_field_dto()
        if existing_field_ids is None:
            existing_field_ids = ["field_1"]

        self.field_storage.get_fields.return_value = [field_data]
        self.field_storage.get_existing_field_ids.return_value = existing_field_ids

    def test_get_active_field_success(self, snapshot):
        # Arrange
        self._setup_get_field_dependencies()

        # Act
        result = self.interactor.get_fields(field_ids=["field_1"])[0]

        snapshot.assert_match(
            repr(result),
            "test_get_active_field_success.txt",
        )

    def test_get_active_field_not_found(self, snapshot):
        # Arrange
        self._setup_get_field_dependencies(
            field_data=None, existing_field_ids=[])
        self.field_storage.get_fields.return_value = []

        # Act
        with pytest.raises(InvalidFieldIdsFound) as exc:
            self.interactor.get_fields(field_ids=["field_1"])

        snapshot.assert_match(
            repr(exc.value),
            "test_get_active_field_not_found.txt",
        )
