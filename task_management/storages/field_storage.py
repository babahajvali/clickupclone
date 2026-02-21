from typing import Optional

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F

from task_management.exceptions.enums import FieldType
from task_management.interactors.dtos import CreateFieldDTO, FieldDTO, \
    UpdateFieldDTO, UpdateFieldValueDTO, TaskFieldValueDTO, CreateFieldValueDTO
from task_management.interactors.storage_interfaces import \
    FieldStorageInterface

from task_management.models import Field, FieldValue


class FieldStorage(FieldStorageInterface):

    @staticmethod
    def _field_dto(field_data: Field) -> FieldDTO:
        return FieldDTO(
            field_id=field_data.field_id,
            field_name=field_data.field_name,
            description=field_data.description,
            field_type=FieldType(field_data.field_type),
            template_id=field_data.template.template_id,
            is_delete=field_data.is_delete,
            order=field_data.order,
            config=field_data.config,
            is_required=field_data.is_required,
            created_by=field_data.created_by.user_id,
        )

    def create_field(
            self, create_field_data: CreateFieldDTO, order: int) -> FieldDTO:

        field_data = Field.objects.create(
            field_name=create_field_data.field_name,
            description=create_field_data.description,
            field_type=create_field_data.field_type.value,
            template_id=create_field_data.template_id,
            order=order,
            config=create_field_data.config,
            is_required=create_field_data.is_required,
            created_by_id=create_field_data.created_by_user_id
        )

        return self._field_dto(field_data=field_data)

    def is_field_name_exists(
            self, field_name: str, template_id: str,
            exclude_field_id: Optional[str]) -> bool:

        field_data = Field.objects.filter(
            field_name=field_name, template_id=template_id)

        if exclude_field_id:
            field_data = field_data.exclude(field_id=exclude_field_id)

        return field_data.exists()

    def get_field_by_id(self, field_id: str) -> FieldDTO | None:
        try:
            field_data = Field.objects.get(field_id=field_id)
            return self._field_dto(field_data=field_data)
        except ObjectDoesNotExist:
            return None

    def update_field(self, field_id: str,
                     update_field_data: UpdateFieldDTO) -> FieldDTO:

        fields_to_update = {}
        if update_field_data.field_name is not None:
            fields_to_update['field_name'] = update_field_data.field_name
        if update_field_data.description is not None:
            fields_to_update['description'] = update_field_data.description
        if update_field_data.config is not None:
            fields_to_update['config'] = update_field_data.config
        if update_field_data.is_required is not None:
            fields_to_update['is_required'] = update_field_data.is_required

        Field.objects.filter(field_id=field_id).update(**fields_to_update)

        field_data = Field.objects.get(field_id=field_id)
        return self._field_dto(field_data=field_data)

    def get_fields_for_template(self, template_id: str) ->\
            list[FieldDTO]:

        fields_data = Field.objects.filter(
            template_id=template_id, is_delete=False
        )
        return [
            self._field_dto(field_data=field_data)
            for field_data in fields_data
        ]

    def shift_fields_down(self, template_id: str, old_order: int,
                          new_order: int):
        Field.objects.filter(
            template_id=template_id,
            is_delete=False,
            order__gt=old_order,
            order__lte=new_order
        ).update(order=F("order") - 1)

    def shift_fields_up(self, template_id: str, new_order: int,
                        old_order: int):
        Field.objects.filter(
            template_id=template_id,
            is_delete=False,
            order__gte=new_order,
            order__lt=old_order
        ).update(order=F("order") + 1)

    def update_field_order(self, field_id: str, new_order: int) -> FieldDTO:
        field_data = Field.objects.get(field_id=field_id)
        field_data.order = new_order
        field_data.save()
        return self._field_dto(field_data=field_data)

    def template_fields_count(self, template_id: str) -> int:
        return Field.objects.filter(
            template_id=template_id, is_delete=False).count()

    def delete_field(self, field_id: str):
        field_data = Field.objects.get(field_id=field_id)
        field_data.is_delete = True
        field_data.save()

        Field.objects.filter(
            template_id=field_data.template.template_id,
            is_delete=False,
            order__gt=field_data.order
        ).update(order=F("order") - 1)

        return self._field_dto(field_data=field_data)

    def create_bulk_fields(
            self, fields_data: list[CreateFieldDTO]) -> list[FieldDTO]:

        fields_to_create = [
            Field(
                field_name=field_data.field_name,
                description=field_data.description,
                field_type=field_data.field_type.value,
                template_id=field_data.template_id,
                order=i + 1,
                config=field_data.config,
                is_required=field_data.is_required,
                created_by_id=field_data.created_by_user_id
            )
            for i, field_data in enumerate(fields_data)
        ]

        created_fields = Field.objects.bulk_create(fields_to_create)
        return [self._field_dto(field) for field in created_fields]

    def update_or_create_task_field_value(
            self, field_value_data: UpdateFieldValueDTO, user_id: str) \
            -> TaskFieldValueDTO:

        obj, created = FieldValue.objects.update_or_create(
            task_id=field_value_data.task_id,
            field_id=field_value_data.field_id,
            defaults={
                'value': field_value_data.value,
                'created_by': user_id
            }
        )

        return TaskFieldValueDTO(
            id=obj.pk,
            task_id=obj.task.task_id,
            field_id=obj.field.field_id,
            value=obj.value,
        )

    def create_bulk_field_values(
            self, create_bulk_field_values: list[CreateFieldValueDTO]):

        field_values_to_create = [
            FieldValue(
                task_id=fv_data.task_id,
                field_id=fv_data.field_id,
                value=fv_data.value,
                created_by_id=fv_data.created_by
            )
            for fv_data in create_bulk_field_values
        ]
        FieldValue.objects.bulk_create(field_values_to_create)

    def get_workspace_id_from_field_id(self, field_id: str) -> str:
        field_data = Field.objects.select_related(
            "template__list__space__workspace").get(field_id=field_id)
        return field_data.template.list.space.workspace.workspace_id

    def get_next_field_order_in_template(self, template_id: str) -> int:
        last_field = Field.objects.filter(
            template_id=template_id,
            is_delete=False).order_by('-order').first()
        next_order = (last_field.order + 1) if last_field else 1

        return next_order
