from django.core.exceptions import ObjectDoesNotExist
from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import TemplateNotFoundType
from task_management.graphql.types.types import FieldType, FieldsType
from task_management.interactors.field_interactors.field_interactors import \
    FieldInteractor
from task_management.storages.field_storage import FieldStorage
from task_management.storages.template_storage import TemplateStorage
from task_management.storages.list_permission_storage import ListPermissionStorage


def get_fields_for_template_resolver(root, info, params):
    template_id = params.template_id

    field_storage = FieldStorage()
    template_storage = TemplateStorage()
    permission_storage = ListPermissionStorage()

    interactor = FieldInteractor(
        field_storage=field_storage,
        template_storage=template_storage,
        permission_storage=permission_storage
    )

    try:
        fields_data = interactor.get_fields_for_template(template_id=template_id)

        fields_output = [
            FieldType(
                field_id=str(field.field_id),
                field_type=field.field_type.value if hasattr(field.field_type, 'value') else field.field_type,
                description=field.description,
                template_id=str(field.template_id),
                field_name=field.field_name,
                order=field.order,
                config=field.config,
                is_required=field.is_required,
                created_by=str(field.created_by)
            ) for field in fields_data
        ]

        return FieldsType(fields=fields_output)

    except custom_exceptions.TemplateNotFoundException as e:
        return TemplateNotFoundType(template_id=e.template_id)

    except ObjectDoesNotExist:
        return TemplateNotFoundType(template_id=template_id)