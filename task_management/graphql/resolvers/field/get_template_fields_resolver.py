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
        fields_dto = interactor.get_template_fields(
            template_id=template_id)

        fields_output = [
            FieldType(
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
            ) for field_dto in fields_dto
        ]

        return FieldsType(fields=fields_output)

    except custom_exceptions.TemplateNotFound as e:
        return TemplateNotFoundType(template_id=e.template_id)
