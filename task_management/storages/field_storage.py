from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import F

from task_management.exceptions.enums import FieldTypeEnum
from task_management.interactors.dtos import CreateFieldDTO, FieldDTO, \
    UpdateFieldDTO
from task_management.interactors.storage_interface.field_storage_interface import \
    FieldStorageInterface
from task_management.models import Template, User, Field


class FieldStorage(FieldStorageInterface):

    @staticmethod
    def _field_dto(field_data: Field) -> FieldDTO:
        field_type = FieldTypeEnum(field_data.field_type)
        return FieldDTO(
            field_id=field_data.field_id,
            field_name=field_data.field_name,
            description=field_data.description,
            field_type=field_type,
            template_id=field_data.template.template_id,
            is_active=field_data.is_active,
            order=field_data.order,
            config=field_data.config,
            is_required=field_data.is_required,
            created_by=field_data.created_by.user_id,
        )

    def create_field(self, create_field_data: CreateFieldDTO) -> FieldDTO:
        template = Template.objects.get(
            template_id=create_field_data.template_id)
        created_by = User.objects.get(user_id=create_field_data.created_by)

        last_field = Field.objects.filter(
            template=template, is_active=True).order_by('-order').first()
        next_order = (last_field.order + 1) if last_field else 1

        field_data = Field.objects.create(
            field_name=create_field_data.field_name,
            description=create_field_data.description,
            field_type=create_field_data.field_type.value,
            template=template,
            order=next_order,
            config=create_field_data.config,
            is_required=create_field_data.is_required,
            created_by=created_by
        )

        return self._field_dto(field_data=field_data)

    def is_field_name_exists(self, field_name: str, template_id: str) -> bool:
        return Field.objects.filter(field_name=field_name,
                                    template_id=template_id).exists()

    def get_field_by_id(self, field_id: str) -> FieldDTO | None:
        try:
            field_data = Field.objects.get(field_id=field_id)

            return self._field_dto(field_data=field_data)
        except ObjectDoesNotExist:
            return None

    def update_field(self, update_field_data: UpdateFieldDTO) -> FieldDTO:
        field_data = Field.objects.get(field_id=update_field_data.field_id)
        if update_field_data.description is not None:
            field_data.description = update_field_data.description

        if update_field_data.field_name is not None:
            field_data.field_name = update_field_data.field_name

        if update_field_data.is_required is not None:
            field_data.is_required = update_field_data.is_required

        if update_field_data.config is not None:
            field_data.config = update_field_data.config
        field_data.save()

        return self._field_dto(field_data=field_data)

    def is_field_exists(self, field_id: str) -> bool:
        return Field.objects.filter(field_id=field_id, is_active=True).exists()

    def check_field_name_except_this_field(self, field_id: str,
                                           field_name: str,
                                           template_id: str) -> bool:
        return Field.objects.filter(
            field_name=field_name, template_id=template_id).exclude(
            field_id=field_id).exists()

    def get_fields_for_template(self, template_id: str) -> list[FieldDTO]:
        fields_data = Field.objects.filter(template_id=template_id,
                                           is_active=True)

        return [self._field_dto(field_data=field_data) for field_data in
                fields_data]

    @transaction.atomic
    def reorder_fields(self, field_id: str, template_id: str,
                       new_order: int) -> FieldDTO:
        field_data = Field.objects.get(field_id=field_id)
        old_order = field_data.order

        if old_order == new_order:
            return self._field_dto(field_data=field_data)

        if new_order > old_order:
            Field.objects.filter(
                template_id=template_id,
                is_active=True,
                order__gt=old_order,
                order__lte=new_order
            ).update(order=F("order") - 1)
        else:
            Field.objects.filter(
                template_id=template_id,
                is_active=True,
                order__gte=new_order,
                order__lt=old_order
            ).update(order=F("order") + 1)

        field_data.order = new_order
        field_data.save()

        return self._field_dto(field_data=field_data)

    def template_fields_count(self, template_id: str) -> int:
        return Field.objects.filter(template_id=template_id,
                                    is_active=True).count()

    def delete_field(self, field_id: str):
        field_data = Field.objects.get(field_id=field_id)
        field_data.is_active = False
        field_data.save()

        current_order = field_data.order
        Field.objects.filter(
            template_id=field_data.template.template_id, is_active=True,
            order__gt=current_order).update(order=F("order") - 1)

        return self._field_dto(field_data=field_data)
