from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import TemplateNotFound
from task_management.exceptions.enums import FieldType
from task_management.interactors.dtos import FieldDTO
from task_management.interactors.fields.get_template_fields_interactor import \
    GetTemplateFieldsInteractor
from task_management.interactors.storage_interfaces.field_storage_interface import (
    FieldStorageInterface,
)
from task_management.interactors.storage_interfaces.template_storage_interface import (
    TemplateStorageInterface,
)


class TestGetFieldForTemplateInteractor:

    def setup_method(self):
        self.field_storage = create_autospec(FieldStorageInterface)
        self.template_storage = create_autospec(TemplateStorageInterface)

        self.interactor = GetTemplateFieldsInteractor(
            field_storage=self.field_storage,
            template_storage=self.template_storage,
        )

    def test_get_fields_for_template_success(self, snapshot):
        template_id = "templates-123"

        expected_fields = [
            FieldDTO(
                field_id="field_1",
                field_type=FieldType.TEXT,
                description="Field 1",
                template_id="tpl_1",
                field_name="Priority",
                is_deleted=False,
                order=1,
                config={},
                is_required=True,
                created_by="user_1",
            ),
            FieldDTO(
                field_id="field_2",
                field_type=FieldType.NUMBER,
                description="Field 2",
                template_id="tpl_1",
                field_name="Estimate",
                is_deleted=False,
                order=2,
                config={},
                is_required=False,
                created_by="user_1",
            ),
        ]

        self.template_storage.validate_template_exists.return_value = True

        self.field_storage.get_fields_for_template.return_value = expected_fields

        result = self.interactor.get_template_fields(template_id)

        snapshot.assert_match(
            repr(result),
            "get_fields_for_template_success.txt"
        )

    def test_get_fields_for_template_not_found(self, snapshot):
        template_id = "non-existent-template"
        self.template_storage.validate_template_exists.return_value = False

        with pytest.raises(TemplateNotFound) as exc:
            self.interactor.get_template_fields(template_id)

        snapshot.assert_match(
            exc.value.template_id,
            "template_not_found.txt"
        )
