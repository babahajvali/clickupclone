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

        return FieldsType(
            fields=[FieldType.from_dto(field) for field in fields_dto])

    except custom_exceptions.TemplateNotFound as e:
        return TemplateNotFoundType(template_id=e.template_id)
