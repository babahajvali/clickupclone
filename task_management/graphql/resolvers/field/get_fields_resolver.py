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

        return FieldsType(
            fields=[FieldType.from_dto(f) for f in fields_dto])

    except custom_exceptions.InvalidFieldIdsFound as e:
        return InvalidFieldIdsType(field_ids=e.field_ids)
