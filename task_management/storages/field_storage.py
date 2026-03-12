from typing import Optional, List

from django.db import transaction
from django.db.models import F

from task_management.exceptions.enums import FieldType, ListEntityType
from task_management.interactors.dtos import CreateFieldDTO, FieldDTO, \
    UpdateFieldDTO, UpdateFieldValueDTO, TaskFieldValueDTO, \
    CreateFieldValueDTO, TaskFieldValuesDTO, FieldValueDTO
from task_management.interactors.storage_interfaces import \
    FieldStorageInterface
from task_management.models import Field, TaskFieldValue, Space, Folder


class FieldStorage(FieldStorageInterface):

    @staticmethod
    def _convert_to_field_dto(field_obj: Field) -> FieldDTO:
        return FieldDTO(
            field_id=field_obj.field_id,
            field_name=field_obj.field_name,
            description=field_obj.description,
            field_type=FieldType(field_obj.field_type),
            template_id=field_obj.template_id,
            is_deleted=field_obj.is_deleted,
            order=field_obj.order,
            config=field_obj.config,
            is_required=field_obj.is_required,
            created_by=field_obj.created_by_id,
        )

    def create_field(
            self, create_field_dto: CreateFieldDTO, order: int) -> FieldDTO:

        field_obj = Field.objects.create(
            field_name=create_field_dto.field_name,
            description=create_field_dto.description,
            field_type=create_field_dto.field_type.value,
            template_id=create_field_dto.template_id,
            order=order,
            config=create_field_dto.config,
            is_required=create_field_dto.is_required,
            created_by_id=create_field_dto.created_by_user_id
        )

        return self._convert_to_field_dto(field_obj=field_obj)

    def is_field_name_exists(
            self, field_name: str, template_id: str,
            excluded_field_id: Optional[str]) -> bool:

        field_obj = Field.objects.filter(
            field_name=field_name, template_id=template_id)

        if excluded_field_id:
            field_obj = field_obj.exclude(field_id=excluded_field_id)

        return field_obj.exists()

    def get_fields(self, field_ids: List[str]) -> List[FieldDTO] | None:

        field_objs = Field.objects.filter(field_id__in=field_ids)
        if not field_objs:
            return None
        return [self._convert_to_field_dto(field_obj=field_data) for
                field_data in field_objs]

    def get_existing_field_ids(self, field_ids: List[str]) -> List[str]:
        existing_field_ids = Field.objects.filter(
            field_id__in=field_ids).values_list('field_id', flat=True)

        return [str(field_id) for field_id in existing_field_ids]

    def update_field(
            self, update_field_dto: UpdateFieldDTO) -> FieldDTO:

        field_properties = {}
        if update_field_dto.field_name is not None:
            field_properties['field_name'] = update_field_dto.field_name
        if update_field_dto.description is not None:
            field_properties['description'] = update_field_dto.description
        if update_field_dto.config is not None:
            field_properties['config'] = update_field_dto.config
        if update_field_dto.is_required is not None:
            field_properties['is_required'] = update_field_dto.is_required

        Field.objects.filter(field_id=update_field_dto.field_id).update(
            **field_properties)

        return self.get_fields(field_ids=[update_field_dto.field_id])[0]

    def get_fields_for_template(self, template_id: str) -> List[FieldDTO]:

        fields_obj = Field.objects.filter(
            template_id=template_id, is_deleted=False
        )
        return [
            self._convert_to_field_dto(field_obj=field_obj)
            for field_obj in fields_obj
        ]

    def get_field_values_by_task_ids(
            self, task_ids: List[str]) -> List[TaskFieldValuesDTO]:
        field_values = TaskFieldValue.objects.filter(task_id__in=task_ids)

        task_values_map = {}
        for fv in field_values:
            if fv.value is None:
                continue
            task_id = str(fv.task_id)
            if task_id not in task_values_map:
                task_values_map[task_id] = []

            task_values_map[task_id].append(
                FieldValueDTO(
                    field_id=str(fv.field_id),
                    value=fv.value
                )
            )
        result = []
        for task_id in task_ids:
            result.append(
                TaskFieldValuesDTO(
                    task_id=str(task_id),
                    values=task_values_map.get(str(task_id), [])
                )
            )
        return result

    def shift_fields_down(
            self, template_id: str, old_order: int, new_order: int):
        Field.objects.filter(
            template_id=template_id,
            is_deleted=False,
            order__gt=old_order,
            order__lte=new_order
        ).update(order=F("order") - 1)

    def shift_fields_up(
            self, template_id: str, new_order: int, old_order: int):
        Field.objects.filter(
            template_id=template_id,
            is_deleted=False,
            order__gte=new_order,
            order__lt=old_order
        ).update(order=F("order") + 1)

    def update_field_order(self, field_id: str, new_order: int) -> FieldDTO:

        Field.objects.filter(field_id=field_id).update(order=new_order)

        return self.get_fields(field_ids=[field_id])[0]

    def template_fields_count(self, template_id: str) -> int:

        return Field.objects.filter(
            template_id=template_id, is_deleted=False).count()

    @transaction.atomic
    def delete_field(self, field_id: str):
        Field.objects.filter(field_id=field_id).update(is_deleted=True)

        field_dto = self.get_fields(field_ids=[field_id])[0]

        Field.objects.filter(
            template_id=field_dto.template_id,
            is_deleted=False,
            order__gt=field_dto.order
        ).update(order=F("order") - 1)

        return field_dto

    def create_bulk_fields(
            self, create_field_dtos: List[CreateFieldDTO]) -> List[FieldDTO]:

        fields_to_create = [
            Field(
                field_name=create_field_dto.field_name,
                description=create_field_dto.description,
                field_type=create_field_dto.field_type.value,
                template_id=create_field_dto.template_id,
                order=i + 1,
                config=create_field_dto.config,
                is_required=create_field_dto.is_required,
                created_by_id=create_field_dto.created_by_user_id
            )
            for i, create_field_dto in enumerate(create_field_dtos)
        ]

        created_fields = Field.objects.bulk_create(fields_to_create)

        return [self._convert_to_field_dto(field) for field in created_fields]

    def update_or_create_task_field_value(
            self, field_value_dto: UpdateFieldValueDTO, user_id: str) \
            -> TaskFieldValueDTO:

        obj, created = TaskFieldValue.objects.update_or_create(
            task_id=field_value_dto.task_id,
            field_id=field_value_dto.field_id,
            defaults={
                'value': field_value_dto.value,
                'created_by_id': user_id
            }
        )

        return TaskFieldValueDTO(
            id=obj.pk,
            task_id=obj.task_id,
            field_id=obj.field_id,
            value=obj.value,
        )

    def create_bulk_field_values(
            self, create_field_value_dtos: List[CreateFieldValueDTO]):

        field_values_to_create = [
            TaskFieldValue(
                task_id=create_field_value_dto.task_id,
                field_id=create_field_value_dto.field_id,
                value=create_field_value_dto.value,
                created_by_id=create_field_value_dto.created_by
            )
            for create_field_value_dto in create_field_value_dtos
        ]
        TaskFieldValue.objects.bulk_create(field_values_to_create)

    def get_workspace_id_from_field_id(self, field_id: str) -> str:
        field_obj = Field.objects.select_related("template__list").values(
            "template__list__entity_type",
            "template__list__entity_id",
        ).get(field_id=field_id)

        entity_type = field_obj["template__list__entity_type"]
        entity_id = field_obj["template__list__entity_id"]

        if entity_type == ListEntityType.SPACE.value:
            return str(Space.objects.values_list(
                "workspace_id", flat=True
            ).get(space_id=entity_id))

        return str(Folder.objects.values_list(
            "space__workspace_id", flat=True
        ).get(folder_id=entity_id))

    def get_last_field_order_in_template(self, template_id: str) -> int:
        last_order = Field.objects.filter(
            template_id=template_id, is_deleted=False
        ).order_by('-order').values_list('order', flat=True).first()

        return last_order or 0
