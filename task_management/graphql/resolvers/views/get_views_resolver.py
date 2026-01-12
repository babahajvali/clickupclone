from task_management.graphql.types.types import ViewType, ViewsType
from task_management.interactors.view_interactors.view_interactors import \
    ViewInteractor
from task_management.storages.view_storage import ViewStorage
from task_management.storages.list_permission_storage import ListPermissionStorage
from task_management.storages.list_storage import ListStorage


def get_all_views_resolver(root, info):
    view_storage = ViewStorage()
    permission_storage = ListPermissionStorage()
    list_storage = ListStorage()

    interactor = ViewInteractor(
        view_storage=view_storage,
        permission_storage=permission_storage,
        list_storage=list_storage
    )

    views_data = interactor.get_views()

    views_output = [
        ViewType(
            view_id=str(view.view_id),
            name=view.name,
            description=view.description,
            view_type=view.view_type,
            created_by=str(view.created_by)
        ) for view in views_data
    ]

    return ViewsType(views=views_output)