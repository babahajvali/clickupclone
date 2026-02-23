from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import FieldNotFound, InactiveField
from task_management.exceptions.enums import FieldType
from task_management.interactors.dtos import FieldDTO
from task_management.interactors.fields.field_interactor import FieldInteractor
from task_management.interactors.storage_interfaces import (
    FieldStorageInterface,
    TemplateStorageInterface,
    WorkspaceStorageInterface,
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
            is_active=True,
            config={"max_length": 10},
            is_required=True,
            created_by="user_1",
        )

    def _get_interactor(self, *, field_data: FieldDTO | None = None):
        field_storage = create_autospec(FieldStorageInterface)
        template_storage = create_autospec(TemplateStorageInterface)
        workspace_storage = create_autospec(WorkspaceStorageInterface)

        if field_data is None:
            field_data = self._get_field_dto()

        field_storage.get_field_by_id.return_value = field_data

        return FieldInteractor(
            field_storage=field_storage,
            template_storage=template_storage,
            workspace_storage=workspace_storage,
        )

    def test_get_active_field_success(self, snapshot):
        interactor = self._get_interactor()

        result = interactor.get_active_field(field_id="field_1")

        snapshot.assert_match(
            repr(result),
            "test_get_active_field_success.txt",
        )

    def test_get_active_field_not_found(self, snapshot):
        interactor = self._get_interactor(field_data=None)
        interactor.field_storage.get_field_by_id.return_value = None

        with pytest.raises(FieldNotFound) as exc:
            interactor.get_active_field(field_id="field_1")

        snapshot.assert_match(
            repr(exc.value.field_id),
            "test_get_active_field_not_found.txt",
        )

    def test_get_active_field_inactive(self, snapshot):
        field_data = self._get_field_dto()
        field_data.is_active = False
        interactor = self._get_interactor(field_data=field_data)

        with pytest.raises(InactiveField) as exc:
            interactor.get_active_field(field_id="field_1")

        snapshot.assert_match(
            repr(exc.value.field_id),
            "test_get_active_field_inactive.txt",
        )
