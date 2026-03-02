from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import ModificationNotAllowed
from task_management.exceptions.enums import Role
from task_management.interactors.dtos import CreateTemplateDTO, TemplateDTO, \
    WorkspaceMemberDTO
from task_management.interactors.storage_interfaces import \
    TemplateStorageInterface, ListStorageInterface, WorkspaceStorageInterface
from task_management.interactors.templates.template_interactor import (
    TemplateInteractor
)


def make_permission(role: Role):
    return WorkspaceMemberDTO(
        id=1,
        workspace_id="workspace_id1",
        role=role,
        user_id="user_id",
        is_active=True,
        added_by="admin"
    )


class TestCreateTemplateInteractor:

    def setup_method(self):
        self.template_storage = create_autospec(TemplateStorageInterface)
        self.list_storage = create_autospec(ListStorageInterface)
        self.workspace_storage = create_autospec(WorkspaceStorageInterface)

        self.interactor = TemplateInteractor(
            template_storage=self.template_storage,
            list_storage=self.list_storage,
            workspace_storage=self.workspace_storage,
        )

    def test_create_template_success(self, snapshot):
        create_template_dto = CreateTemplateDTO(
            name="three",
            description="Serious inside else memory if six.",
            list_id="5ba91faf-7a02-4204-b7c1-bd874da5e709",
            created_by="cca5a5a1-9e4d-4e3c-9846-d424c17c6279",
        )

        template_dto = TemplateDTO(
            template_id="23c6612f-4826-4673-a3a7-711a81332876",
            name=create_template_dto.name,
            list_id=create_template_dto.list_id,
            description=create_template_dto.description,
            created_by=create_template_dto.created_by,
        )

        self.list_storage.get_list.return_value = type(
            "List", (), {"is_deleted": False}
        )()

        self.template_storage.create_template.return_value = template_dto
        self.workspace_storage.get_workspace_member.return_value = type(
            "WorkspaceMember", (), {"is_active": True, "role": Role.MEMBER}
        )()

        result = self.interactor.create_template(create_template_dto)

        snapshot.assert_match(
            repr(result),
            "create_template_success.json"
        )

    def test_create_template_list_not_found(self):
        # Arrange
        create_template_dto = CreateTemplateDTO(
            name="Template name",
            description="Template description",
            list_id="list_1",
            created_by="user_1",
        )
        self.list_storage.get_list.return_value = None

        # Act & Assert
        with pytest.raises(Exception):
            self.interactor.create_template(create_template_dto)

        self.template_storage.create_template.assert_not_called()

    def test_create_template_permission_denied(self):
        create_template_dto = CreateTemplateDTO(
            name="Template name",
            description="Template description",
            list_id="list_1",
            created_by="user_1",
        )

        self.list_storage.get_list.return_value = type(
            "List", (), {"is_deleted": False}
        )()

        self.workspace_storage.get_workspace_member.return_value = (
            make_permission(Role.GUEST))

        with pytest.raises(ModificationNotAllowed):
            self.interactor.create_template(create_template_dto)

        self.template_storage.create_template.assert_not_called()
