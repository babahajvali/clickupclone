from unittest.mock import create_autospec
import pytest
from faker import Faker

from task_management.exceptions.custom_exceptions import \
    ModificationNotAllowed
from task_management.exceptions.enums import Permissions
from task_management.interactors.dtos import UserListPermissionDTO
from task_management.interactors.storage_interfaces import \
    ListStorageInterface, TemplateStorageInterface,  \
    SpaceStorageInterface, WorkspaceStorageInterface
from task_management.interactors.template.template_interactor import \
    TemplateInteractor
from task_management.tests.factories.interactor_factory import (
    TemplateDTOFactory
)

Faker.seed(0)


def make_permission(permission_type: Permissions):
    return UserListPermissionDTO(
        id=1,
        list_id="list_id",
        permission_type=permission_type,
        user_id="user_id",
        is_active=True,
        added_by="admin"
    )


class TestUpdateTemplateInteractor:

    def setup_method(self):
        self.template_storage = create_autospec(TemplateStorageInterface)
        self.list_storage = create_autospec(ListStorageInterface)
        self.space_storage = create_autospec(SpaceStorageInterface)
        self.workspace_storage = create_autospec(WorkspaceStorageInterface)

        self.interactor = TemplateInteractor(
            template_storage=self.template_storage,
            list_storage=self.list_storage,
            workspace_storage=self.workspace_storage,
        )
    @staticmethod
    def _mock_active_list(self):
        return type("List", (), {"is_active": True})()

    @staticmethod
    def _mock_template(self):
        return type("Template", (), {"list_id": "list_123"})()

    def test_update_template_success(self, snapshot):
        template_id = "template_id"
        name = "name"
        description = "description"
        list_id = "list_id1"

        updated_template = TemplateDTOFactory(
            template_id=template_id,
            name=name,
            list_id=list_id,
            description=description,
        )

        self.template_storage.get_template_by_id.return_value = self._mock_template()
        self.list_storage.get_active_list.return_value = self._mock_active_list()
        self.workspace_storage.get_user_permission_for_list.return_value = (
            make_permission(Permissions.FULL_EDIT)
        )
        self.template_storage.validate_template_exists.return_value = False
        self.template_storage.update_template.return_value = updated_template

        result = self.interactor.update_template(template_id=template_id,
                                                 user_id="user_id", name=name,
                                                 description=description)

        snapshot.assert_match(
            repr(result),
            "update_template_success.json"
        )

    def test_update_template_template_not_found(self):
        template_id = "template_id"
        name = "name"
        description = "description"

        self.template_storage.get_template_by_id.side_effect = Exception(
            "Template not found"
        )

        with pytest.raises(Exception):
            self.interactor.update_template(template_id=template_id,
                                            user_id="user_id", name=name,
                                            description=description)
        self.template_storage.update_template.assert_not_called()

    def test_update_template_list_not_found(self):
        template_id = "template_id"
        name = "name"
        description = "description"

        self.template_storage.get_template_by_id.return_value = self._mock_template()
        self.list_storage.get_active_list.return_value = None

        with pytest.raises(Exception):
            self.interactor.update_template(template_id=template_id,
                                            user_id="user_id", name=name,
                                            description=description)

        self.template_storage.update_template.assert_not_called()

    def test_update_template_permission_denied(self):
        template_id = "template_id"
        name = "name"
        description = "description"

        self.template_storage.get_template_by_id.return_value = self._mock_template()
        self.list_storage.get_active_list.return_value = self._mock_active_list()
        with pytest.raises(ModificationNotAllowed):
            self.interactor.update_template(template_id=template_id,
                                            user_id="user_id", name=name,
                                            description=description)

        self.template_storage.update_template.assert_not_called()
