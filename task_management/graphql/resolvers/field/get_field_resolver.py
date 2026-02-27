from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import FieldNotFoundType
from task_management.graphql.types.types import FieldType
from task_management.interactors.fields.get_field_interactor import \
    GetFieldInteractor
from task_management.storages import FieldStorage


def get_field_resolver(root, info, params):
    field_id = params.field_id

    field_storage = FieldStorage()

    interactor = GetFieldInteractor(
        field_storage=field_storage,
    )
    try:
        field_data = interactor.get_field(field_id=field_id)

        return FieldType(
            field_id=field_data.field_id,
            field_type=field_data.field_type.value,
            description=field_data.description,
            template_id=field_data.template_id,
            field_name=field_data.field_name,
            order=field_data.order,
            config=field_data.config,
            is_deleted=field_data.is_deleted,
            is_required=field_data.is_required,
            created_by=field_data.created_by
        )

    except custom_exceptions.FieldNotFound as e:
        return FieldNotFoundType(field_id=e.field_id)
