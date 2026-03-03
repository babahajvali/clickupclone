from task_management.graphql.types.types import ViewType, ViewsType
from task_management.storages import ViewStorage


def get_all_views_resolver(root, info):
    view_storage = ViewStorage()

    views_data = view_storage.get_all_views()

    views_output = [
        ViewType(
            view_id=view.view_id,
            name=view.name,
            description=view.description,
            view_type=view.view_type.value,
            created_by=view.created_by
        ) for view in views_data
    ]

    return ViewsType(views=views_output)
