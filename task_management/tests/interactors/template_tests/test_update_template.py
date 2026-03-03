from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import (
    ModificationNotAllowed,
    TemplateNotFound,
)
from task_management.exceptions.enums import Role
from task_management.interactors.dtos import WorkspaceMemberDTO, TemplateDTO
from task_management.interactors.storage_interfaces import \
    ListStorageInterface, TemplateStorageInterface, WorkspaceStorageInterface
from task_management.interactors.templates.update_template_interactor import \
    TemplateInteractor


def make_permission(role: Role) -> WorkspaceMemberDTO:
    return WorkspaceMemberDTO(
        id=1,
        workspace_id="workspace_id1",
        role=role,
        user_id="user_id",
        is_active=True,
        added_by="admin"
    )


def make_template() -> object:
    return type("Template", (), {"list_id": "list_123"})()


def make_active_list() -> object:
    return type("List", (), {"is_deleted": False})()


def make_updated_template() -> TemplateDTO:
    return TemplateDTO(
        template_id="template_id",
        name="name",
        list_id="list_id1",
        description="description",
        created_by="a0116be5-ab0c-4681-88f8-e3d0d3290a4c",
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

    def _setup_dependencies(self, role: Role = Role.ADMIN):
        self.template_storage.get_template_by_id.return_value = make_template()
        self.list_storage.get_list.return_value = make_active_list()
        self.workspace_storage.get_workspace_member.return_value = make_permission(
            role=role
        )
        self.template_storage.update_template.return_value = make_updated_template()

    def test_update_template_success(self, snapshot):
        self._setup_dependencies()
        result = self.interactor.update_template(
            template_id="template_id",
            user_id="user_id",
            name="name",
            description="description",
        )

        snapshot.assert_match(
            repr(result),
            "update_template_success.json"
        )

    def test_update_template_template_not_found(self):
        self._setup_dependencies()
        self.template_storage.validate_template_exists.return_value = False

        with pytest.raises(TemplateNotFound):
            self.interactor.update_template(
                template_id="template_id",
                user_id="user_id",
                name="name",
                description="description",
            )
        self.template_storage.update_template.assert_not_called()

    def test_update_template_permission_denied(self):
        self._setup_dependencies(role=Role.GUEST)
        with pytest.raises(ModificationNotAllowed):
            self.interactor.update_template(
                template_id="template_id",
                user_id="user_id",
                name="name",
                description="description",
            )

        self.template_storage.update_template.assert_not_called()
