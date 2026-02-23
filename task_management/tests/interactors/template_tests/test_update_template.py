from unittest.mock import create_autospec
import pytest
from faker import Faker

from task_management.exceptions.custom_exceptions import \
    ModificationNotAllowed, ListNotFound
from task_management.exceptions.enums import Permissions, Role
from task_management.interactors.dtos import UserListPermissionDTO, \
    WorkspaceMemberDTO
from task_management.interactors.storage_interfaces import \
    ListStorageInterface, TemplateStorageInterface,  \
    SpaceStorageInterface, WorkspaceStorageInterface
from task_management.interactors.templates.template_interactor import \
    TemplateInteractor
from task_management.tests.factories.interactor_factory import (
    TemplateDTOFactory
)

Faker.seed(0)


def make_permission(role: Role):
    return WorkspaceMemberDTO(
        id=1,
        workspace_id="workspace_id1",
        role=role,
        user_id="user_id",
        is_active=True,
        added_by="admin"
    )


class TestUpdateTemplateInteractor:

    def setup_method(self):
        self.template_storage = create_autospec(TemplateStorageInterface)
        self.list_storage = create_autospec(ListStorageInterface)
        self.workspace_storage = create_autospec(WorkspaceStorageInterface)

        self.interactor = TemplateInteractor(
            template_storage=self.template_storage,
            list_storage=self.list_storage,
            workspace_storage=self.workspace_storage,
        )
    @staticmethod
    def _mock_active_list():
        return type("List", (), {"is_deleted": False})()

    @staticmethod
    def _mock_template():
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
        self.list_storage.get_list.return_value = self._mock_active_list()
        self.workspace_storage.get_workspace_member.return_value = (
            make_permission(role=Role.ADMIN)
        )
        self.template_storage.validate_template_exists.return_value = True
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

    def test_update_template_permission_denied(self):
        template_id = "template_id"
        name = "name"
        description = "description"

        self.template_storage.get_template_by_id.return_value = self._mock_template()
        self.workspace_storage.get_workspace_member.return_value = make_permission(role=Role.GUEST)
        self.list_storage.get_list.return_value = self._mock_active_list()
        with pytest.raises(ModificationNotAllowed):
            self.interactor.update_template(template_id=template_id,
                                            user_id="user_id", name=name,
                                            description=description)

        self.template_storage.update_template.assert_not_called()
