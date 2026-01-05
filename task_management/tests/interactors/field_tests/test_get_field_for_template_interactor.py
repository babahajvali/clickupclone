import pytest
from unittest.mock import create_autospec

from task_management.interactors.field_interactors.field_interactors import \
    FieldInteractor
from task_management.interactors.storage_interface.field_storage_interface import FieldStorageInterface
from task_management.interactors.storage_interface.list_permission_storage_interface import \
    ListPermissionStorageInterface
from task_management.interactors.storage_interface.template_storage_interface import TemplateStorageInterface
from task_management.tests.factories.interactor_factory import FieldDTOFactory


class TestGetFieldForTemplateInteractor:

    def setup_method(self):
        self.field_storage = create_autospec(FieldStorageInterface)
        self.template_storage = create_autospec(TemplateStorageInterface)
        self.permission_storage = create_autospec(ListPermissionStorageInterface)
        
        self.interactor = FieldInteractor(
            field_storage=self.field_storage,
            template_storage=self.template_storage,
            permission_storage=self.permission_storage
        )

    def test_get_fields_for_template_success(self, snapshot):
        template_id = "template-123"

        expected_fields = [
            FieldDTOFactory(),
            FieldDTOFactory()
        ]

        self.template_storage.get_template_exist.return_value = type("Template",(),{"list_id": "list-123"})()

        self.field_storage.get_fields_for_template.return_value = expected_fields

        result = self.interactor.get_fields_for_template(template_id)

        snapshot.assert_match(
            repr(result),
            "get_fields_for_template_success.txt"
        )

    def test_get_fields_for_template_not_found(self, snapshot):
        template_id = "non-existent-template"

        self.template_storage.get_template_exist.return_value = False

        with pytest.raises(Exception) as exc:
            self.interactor.get_fields_for_template(template_id)

        snapshot.assert_match(
            repr(exc.value),
            "template_not_found.txt"
        )

