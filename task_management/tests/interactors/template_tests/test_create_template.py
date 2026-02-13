from unittest.mock import create_autospec, patch

import pytest
from faker import Faker

from task_management.exceptions.enums import Role
from task_management.interactors.storage_interfaces import \
    WorkspaceStorageInterface
from task_management.interactors.storage_interfaces.field_storage_interface import (
    FieldStorageInterface
)
from task_management.interactors.storage_interfaces.list_storage_interface import (
    ListStorageInterface
)
from task_management.interactors.storage_interfaces.space_storage_interface import \
    SpaceStorageInterface
from task_management.interactors.storage_interfaces.template_storage_interface import (
    TemplateStorageInterface
)
from task_management.interactors.template.template_interactor import (
    TemplateInteractor
)
from task_management.tests.factories.interactor_factory import (
    CreateTemplateDTOFactory,
    TemplateDTOFactory
)

Faker.seed(0)


class TestCreateTemplateInteractor:

    def setup_method(self):
        self.field_storage = create_autospec(FieldStorageInterface)
        self.template_storage = create_autospec(TemplateStorageInterface)
        self.list_storage = create_autospec(ListStorageInterface)
        self.space_storage = create_autospec(SpaceStorageInterface)
        self.workspace_storage = create_autospec(WorkspaceStorageInterface)

        self.interactor = TemplateInteractor(
            field_storage=self.field_storage,
            template_storage=self.template_storage,
            list_storage=self.list_storage,
            space_storage=self.space_storage,
            workspace_storage=self.workspace_storage,
        )

    def test_create_template_success(self, snapshot):
        create_template_dto = CreateTemplateDTOFactory()

        template_dto = TemplateDTOFactory(
            name=create_template_dto.name,
            list_id=create_template_dto.list_id,
            description=create_template_dto.description,
        )

        self.list_storage.get_list.return_value = type(
            "List", (), {"is_active": True}
        )()

        self.template_storage.create_template.return_value = template_dto

        result = self.interactor.create_template(create_template_dto)

        snapshot.assert_match(
            repr(result),
            "create_template_success.json"
        )

    def test_create_template_list_not_found(self):
        # Arrange
        create_template_dto = CreateTemplateDTOFactory()
        self.list_storage.get_list.return_value = None

        # Act & Assert
        with pytest.raises(Exception):
            self.interactor.create_template(create_template_dto)

        self.template_storage.create_template.assert_not_called()

    def test_create_template_permission_denied(self):
        create_template_dto = CreateTemplateDTOFactory()

        self.list_storage.get_list.return_value = type(
            "List", (), {"is_active": True}
        )()

        self.workspace_storage.get_workspace_member.return_value = (
            Role.MEMBER
        )

        with pytest.raises(Exception):
            self.interactor.create_template(create_template_dto)

        self.template_storage.create_template.assert_not_called()
