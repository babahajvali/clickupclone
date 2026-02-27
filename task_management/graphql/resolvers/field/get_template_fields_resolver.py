from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import TemplateNotFoundType
from task_management.graphql.types.types import FieldType, FieldsType

from task_management.interactors.fields.get_template_fields_interactor import \
    GetTemplateFieldsInteractor
from task_management.storages import FieldStorage, TemplateStorage, \
    ListStorage


def get_fields_for_template_resolver(root, info, params):
    list_id = params.list_id

    field_storage = FieldStorage()
    template_storage = TemplateStorage()
    list_storage = ListStorage()

    interactor = GetTemplateFieldsInteractor(
        field_storage=field_storage,
        template_storage=template_storage,
    )

    try:
        template_id = list_storage.get_template_id_by_list_id(list_id=list_id)
        fields_data = interactor.get_fields_for_template(
            template_id=template_id)

        fields_output = [
            FieldType(
                field_id=field.field_id,
                field_type=field.field_type.value,
                description=field.description,
                template_id=field.template_id,
                field_name=field.field_name,
                order=field.order,
                config=field.config,
                is_deleted=field.is_deleted,
                is_required=field.is_required,
                created_by=field.created_by
            ) for field in fields_data
        ]

        return FieldsType(fields=fields_output)

    except custom_exceptions.TemplateNotFound as e:
        return TemplateNotFoundType(template_id=e.template_id)
