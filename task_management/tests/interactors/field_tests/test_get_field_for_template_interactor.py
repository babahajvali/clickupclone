import pytest
from unittest.mock import create_autospec

from task_management.exceptions.custom_exceptions import \
    TemplateNotFound
from task_management.interactors.fields.field_interactor import \
    FieldInteractor
from task_management.interactors.storage_interfaces import \
    WorkspaceStorageInterface
from task_management.interactors.storage_interfaces.field_storage_interface import FieldStorageInterface
from task_management.interactors.storage_interfaces.template_storage_interface import TemplateStorageInterface

from task_management.tests.factories.interactor_factory import FieldDTOFactory


class TestGetFieldForTemplateInteractor:

    def setup_method(self):
        self.field_storage = create_autospec(FieldStorageInterface)
        self.template_storage = create_autospec(TemplateStorageInterface)
        self.workspace_storage = create_autospec(WorkspaceStorageInterface)
        
        self.interactor = FieldInteractor(
            field_storage=self.field_storage,
            template_storage=self.template_storage,
            workspace_storage=self.workspace_storage,
        )

    def test_get_fields_for_template_success(self, snapshot):
        template_id = "templates-123"

        expected_fields = [
            FieldDTOFactory(),
            FieldDTOFactory()
        ]

        self.template_storage.validate_template_exists.return_value = True

        self.field_storage.get_active_fields_for_template.return_value = expected_fields

        result = self.interactor.get_active_fields_for_template(template_id)

        snapshot.assert_match(
            repr(result),
            "get_fields_for_template_success.txt"
        )

    def test_get_fields_for_template_not_found(self, snapshot):
        template_id = "non-existent-template"
        self.template_storage.validate_template_exists.return_value = False

        with pytest.raises(TemplateNotFound) as exc:
            self.interactor.get_active_fields_for_template(template_id)

        snapshot.assert_match(
            exc.value.template_id,
            "template_not_found.txt"
        )
