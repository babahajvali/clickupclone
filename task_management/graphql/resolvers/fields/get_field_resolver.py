from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import FieldNotFoundType
from task_management.graphql.types.types import FieldType
from task_management.interactors.field_interactors.field_interactors import \
    FieldInteractor
from task_management.storages.field_storage import FieldStorage
from task_management.storages.list_permission_storage import \
    ListPermissionStorage
from task_management.storages.list_storage import ListStorage
from task_management.storages.space_storage import SpaceStorage
from task_management.storages.template_storage import TemplateStorage
from task_management.storages.workspace_member import WorkspaceMemberStorage


def get_field_resolver(root, info, params):
    field_id = params.field_id

    field_storage = FieldStorage()
    template_storage = TemplateStorage()
    list_storage = ListStorage()
    workspace_member_storage = WorkspaceMemberStorage()
    space_storage = SpaceStorage()

    interactor = FieldInteractor(
        field_storage=field_storage,
        template_storage=template_storage,
        list_storage=list_storage,
        workspace_member_storage=workspace_member_storage,
        space_storage=space_storage,
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
            is_required=field_data.is_required,
            created_by=field_data.created_by
        )

    except custom_exceptions.FieldNotFoundException as e:
        return FieldNotFoundType(field_id=e.field_id)
