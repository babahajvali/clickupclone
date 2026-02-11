import pytest
from unittest.mock import create_autospec

from task_management.exceptions.custom_exceptions import \
    TemplateNotFoundException
from task_management.interactors.field_interactors.field_interactors import \
    FieldInteractor
from task_management.interactors.storage_interfaces.field_storage_interface import FieldStorageInterface
from task_management.interactors.storage_interfaces.list_permission_storage_interface import \
    ListPermissionStorageInterface
from task_management.interactors.storage_interfaces.list_storage_interface import \
    ListStorageInterface
from task_management.interactors.storage_interfaces.space_storage_interface import \
    SpaceStorageInterface
from task_management.interactors.storage_interfaces.template_storage_interface import TemplateStorageInterface
from task_management.interactors.storage_interfaces.workspace_member_storage_interface import \
    WorkspaceMemberStorageInterface
from task_management.tests.factories.interactor_factory import FieldDTOFactory


class TestGetFieldForTemplateInteractor:

    def setup_method(self):
        self.field_storage = create_autospec(FieldStorageInterface)
        self.template_storage = create_autospec(TemplateStorageInterface)
        self.workspace_member_storage = create_autospec(WorkspaceMemberStorageInterface)
        self.list_storage = create_autospec(ListStorageInterface)
        self.space_storage = create_autospec(SpaceStorageInterface)
        
        self.interactor = FieldInteractor(
            field_storage=self.field_storage,
            template_storage=self.template_storage,
            workspace_member_storage=self.workspace_member_storage,
            list_storage=self.list_storage,
            space_storage=self.space_storage
        )

    def test_get_fields_for_template_success(self, snapshot):
        list_id = "list-123"
        template_id = "template-123"

        expected_fields = [
            FieldDTOFactory(),
            FieldDTOFactory()
        ]

        self.template_storage.get_template_by_id.return_value = type("Template", (), {"list_id": "list-123"})()

        self.field_storage.get_fields_for_template.return_value = expected_fields

        result = self.interactor.get_fields_for_template(template_id)

        snapshot.assert_match(
            repr(result),
            "get_fields_for_template_success.txt"
        )

    def test_get_fields_for_template_not_found(self, snapshot):
        template_id = "non-existent-template"
        list_id = "list-123"

        self.interactor.validate_list_is_active.return_value = True

        self.list_storage.get_template_id_by_list_id.return_value = template_id

        self.template_storage.get_template_by_id.return_value = False

        with pytest.raises(TemplateNotFoundException) as exc:
            self.interactor.get_fields_for_template(list_id=list_id)

        snapshot.assert_match(
            exc.value.template_id,
            "template_not_found.txt"
        )


