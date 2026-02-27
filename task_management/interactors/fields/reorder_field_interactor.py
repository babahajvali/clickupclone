from django.db import transaction

from task_management.decorators.caching_decorators import \
    invalidate_interactor_cache
from task_management.exceptions.custom_exceptions import InvalidOrder
from task_management.interactors.dtos import FieldDTO
from task_management.interactors.storage_interfaces import \
    FieldStorageInterface, TemplateStorageInterface, WorkspaceStorageInterface
from task_management.mixins import TemplateValidationMixin, \
    WorkspaceValidationMixin, FieldValidationMixin


class ReorderFieldInteractor:

    def __init__(self, field_storage: FieldStorageInterface,
                 template_storage: TemplateStorageInterface,
                 workspace_storage: WorkspaceStorageInterface):
        self.field_storage = field_storage
        self.template_storage = template_storage
        self.workspace_storage = workspace_storage

    @property
    def template_mixin(self) -> TemplateValidationMixin:
        return TemplateValidationMixin(template_storage=self.template_storage)

    @property
    def workspace_mixin(self) -> WorkspaceValidationMixin:
        return WorkspaceValidationMixin(
            workspace_storage=self.workspace_storage)

    @property
    def field_mixin(self) -> FieldValidationMixin:
        return FieldValidationMixin(field_storage=self.field_storage)

    @transaction.atomic
    @invalidate_interactor_cache(cache_name="fields")
    def reorder_field(
            self, field_id: str, template_id: str, new_order: int,
            user_id: str) -> FieldDTO:

        self.template_mixin.check_template_exists(template_id=template_id)
        self.field_mixin.check_field_is_not_deleted(field_id=field_id)
        self._check_user_has_edit_access_to_template(
            template_id=template_id, user_id=user_id
        )
        self.check_field_order(
            template_id=template_id, order=new_order
        )

        field_dto = self.field_storage.get_field(field_id=field_id)
        old_order = field_dto.order

        if old_order == new_order:
            return field_dto

        return self._reorder_field_positions(
            template_id=template_id, new_order=new_order, old_order=old_order,
            field_id=field_id
        )

    def _check_user_has_edit_access_to_template(
            self, template_id: str, user_id: str):
        workspace_id = self.template_storage.get_workspace_id_from_template_id(
            template_id=template_id)

        self.workspace_mixin.check_user_has_edit_access_to_workspace(
            workspace_id=workspace_id, user_id=user_id)

    def check_field_order(self, template_id: str, order: int):

        if order < 1:
            raise InvalidOrder(order=order)

        fields_count = self.field_storage.template_fields_count(
            template_id=template_id)

        if order > fields_count:
            raise InvalidOrder(order=order)

    def _reorder_field_positions(self, template_id: str, new_order: int,
                                 old_order: int, field_id: str):

        self.reorder_field_positions_except_current(
            template_id=template_id,
            new_order=new_order,
            old_order=old_order
        )

        return self.field_storage.update_field_order(
            field_id=field_id,
            new_order=new_order
        )

    def reorder_field_positions_except_current(
            self, template_id: str, new_order: int, old_order: int):

        if new_order > old_order:
            self.field_storage.shift_fields_down(
                template_id=template_id,
                old_order=old_order,
                new_order=new_order)
        else:
            self.field_storage.shift_fields_up(
                template_id=template_id,
                new_order=new_order,
                old_order=old_order)
