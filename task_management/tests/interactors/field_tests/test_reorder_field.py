import pytest
from unittest.mock import create_autospec

from task_management.exceptions.enums import FieldType, Role
from task_management.interactors.dtos import FieldDTO, WorkspaceMemberDTO
from task_management.interactors.fields.field_interactor import FieldInteractor
from task_management.interactors.storage_interfaces import (
    FieldStorageInterface,
    TemplateStorageInterface,
    WorkspaceStorageInterface,
)
from task_management.exceptions.custom_exceptions import (
    TemplateNotFound,
    FieldNotFound,
    DeletedFieldException,
    ModificationNotAllowed,
    InvalidOrder,
)


def make_field(order=1, is_deleted=False, template_id="template_1"):
    return type(
        "Field",
        (),
        {
            "field_id": "field_1",
            "order": order,
            "is_deleted": is_deleted,
            "template_id": template_id,
        },
    )()


def make_permission(role: Role):
    return WorkspaceMemberDTO(
        id=1,
        workspace_id="workspace_1",
        role=role,
        user_id="user_1",
        is_active=True,
        added_by="admin"
    )


class TestReorderFieldInteractor:

    def setup_method(self):
        self.field_storage = create_autospec(FieldStorageInterface)
        self.template_storage = create_autospec(TemplateStorageInterface)
        self.workspace_storage = create_autospec(WorkspaceStorageInterface)

        self.interactor = FieldInteractor(
            field_storage=self.field_storage,
            template_storage=self.template_storage,
            workspace_storage=self.workspace_storage,
        )

    def _setup_dependencies(
            self, template_exists=True, field_active=True,
            role=Role.ADMIN, field_order=1, fields_count=5):

        # template
        self.template_storage.validate_template_exists.return_value = template_exists

        # field
        self.field_storage.get_field.return_value = (
            make_field(order=field_order, is_deleted=False)
            if field_active
            else None
        )

        self.template_storage.get_workspace_id_from_template_id.return_value = (
            "workspace_1"
        )
        self.workspace_storage.get_workspace_member.return_value = make_permission(
            role=role
        )

        self.field_storage.template_fields_count.return_value = fields_count

        expected = FieldDTO(
            field_id="field_1",
            field_type=FieldType.TEXT,
            description="Reordered field",
            template_id="template_1",
            field_name="Priority",
            is_deleted=False,
            order=field_order,
            config={},
            is_required=True,
            created_by="user_1",
        )
        self.field_storage.update_field_order.return_value = expected
        return expected


    def test_reorder_field_success(self, snapshot):
        expected = self._setup_dependencies(field_order=1)

        result = self.interactor.reorder_field(
            field_id="field_1",
            template_id="template_1",
            new_order=3,
            user_id="user_1"
        )

        assert result == expected
        self.field_storage.update_field_order.assert_called_once_with(
            field_id="field_1", new_order=3)
        snapshot.assert_match(repr(result), "reorder_field_success.txt")

    def test_reorder_field_same_order_returns_early(self):
        self._setup_dependencies(field_order=2)

        result = self.interactor.reorder_field(
            field_id="field_1",
            template_id="template_1",
            new_order=2,
            user_id="user_1"
        )

        # should return early without calling update
        self.field_storage.update_field_order.assert_not_called()


    def test_reorder_field_template_not_found(self, snapshot):
        # Arrange
        self.template_storage.validate_template_exists.return_value = False

        # Act
        with pytest.raises(TemplateNotFound) as exc:
            self.interactor.reorder_field(
                field_id="field_1",
                template_id="bad_template",
                new_order=2,
                user_id="user_1"
            )

        snapshot.assert_match(repr(exc.value), "reorder_field_template_not_found.txt")


    def test_reorder_field_not_found(self, snapshot):
        # Arrange
        self.template_storage.validate_template_exists.return_value = True
        self.field_storage.get_field.return_value = None

        # Act
        with pytest.raises(FieldNotFound) as exc:
            self.interactor.reorder_field(
                field_id="bad_field",
                template_id="template_1",
                new_order=2,
                user_id="user_1"
            )

        snapshot.assert_match(repr(exc.value), "reorder_field_not_found.txt")


    def test_reorder_field_inactive(self, snapshot):
        # Arrange
        self.template_storage.validate_template_exists.return_value = True
        self.field_storage.get_field.return_value = make_field(is_deleted=True)

        # Act
        with pytest.raises(DeletedFieldException) as exc:
            self.interactor.reorder_field(
                field_id="field_1",
                template_id="template_1",
                new_order=2,
                user_id="user_1"
            )

        snapshot.assert_match(repr(exc.value), "reorder_field_inactive.txt")


    def test_reorder_field_invalid_order_low(self, snapshot):
        self._setup_dependencies(fields_count=3)

        with pytest.raises(InvalidOrder) as exc:
            self.interactor.reorder_field(
                field_id="field_1",
                template_id="template_1",
                new_order=0,  # below minimum
                user_id="user_1"
            )

        snapshot.assert_match(repr(exc.value), "reorder_field_invalid_order_low.txt")

    def test_reorder_field_invalid_order_high(self, snapshot):
        self._setup_dependencies(fields_count=3)

        with pytest.raises(InvalidOrder) as exc:
            self.interactor.reorder_field(
                field_id="field_1",
                template_id="template_1",
                new_order=99,  # above max
                user_id="user_1"
            )

        snapshot.assert_match(repr(exc.value), "reorder_field_invalid_order_high.txt")


    def test_reorder_field_permission_denied(self, snapshot):
        self._setup_dependencies(role=Role.GUEST)

        with pytest.raises(ModificationNotAllowed) as exc:
            self.interactor.reorder_field(
                field_id="field_1",
                template_id="template_1",
                new_order=2,
                user_id="user_1"
            )

        snapshot.assert_match(repr(exc.value), "reorder_field_permission_denied.txt")