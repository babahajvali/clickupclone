from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import InvalidFieldIdsType
from task_management.graphql.types.types import FieldType, FieldsType
from task_management.interactors.fields.get_fields_interactor import \
    GetFieldsInteractor
from task_management.storages import FieldStorage


def get_fields_resolver(root, info, params):
    field_ids = params.field_ids

    field_storage = FieldStorage()

    interactor = GetFieldsInteractor(
        field_storage=field_storage,
    )
    try:
        fields_dto = interactor.get_fields(field_ids=field_ids)

        result = [FieldType(
            field_id=field_dto.field_id,
            field_type=field_dto.field_type.value,
            description=field_dto.description,
            template_id=field_dto.template_id,
            field_name=field_dto.field_name,
            order=field_dto.order,
            config=field_dto.config,
            is_deleted=field_dto.is_deleted,
            is_required=field_dto.is_required,
            created_by=field_dto.created_by
        ) for field_dto in fields_dto]

        return FieldsType(fields=result)

    except custom_exceptions.InvalidFieldIdsFound as e:
        return InvalidFieldIdsType(field_ids=e.field_ids)
