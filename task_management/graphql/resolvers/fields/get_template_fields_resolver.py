from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import TemplateNotFoundType
from task_management.graphql.types.types import FieldType, FieldsType
from task_management.interactors.field.field_interactor import \
    FieldInteractor
from task_management.storages.field_storage import FieldStorage
from task_management.storages.list_storage import ListStorage
from task_management.storages.space_storage import SpaceStorage
from task_management.storages.template_storage import TemplateStorage
from task_management.storages.workspace_storage import WorkspaceStorage


def get_fields_for_template_resolver(root, info, params):
    list_id = params.list_id

    field_storage = FieldStorage()
    template_storage = TemplateStorage()
    list_storage = ListStorage()
    workspace_storage = WorkspaceStorage()
    space_storage = SpaceStorage()

    interactor = FieldInteractor(
        field_storage=field_storage,
        template_storage=template_storage,
        list_storage=list_storage,
        space_storage=space_storage,
        workspace_storage=workspace_storage,
    )

    try:
        fields_data = interactor.get_fields_for_template(list_id=list_id)

        fields_output = [
            FieldType(
                field_id=field.field_id,
                field_type=field.field_type.value,
                description=field.description,
                template_id=field.template_id,
                field_name=field.field_name,
                order=field.order,
                config=field.config,
                is_active=field.is_active,
                is_required=field.is_required,
                created_by=field.created_by
            ) for field in fields_data
        ]

        return FieldsType(fields=fields_output)

    except custom_exceptions.TemplateNotFoundException as e:
        return TemplateNotFoundType(template_id=e.template_id)