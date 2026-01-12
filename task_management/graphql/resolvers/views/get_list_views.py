from task_management.graphql.types.types import ListViewType, ListViewsType
from task_management.interactors.view_interactors.list_view_interactors import \
    ListViewInteractor
from task_management.storages.list_permission_storage import \
    ListPermissionStorage
from task_management.storages.list_storage import ListStorage
from task_management.storages.list_view_storage import ListViewStorage
from task_management.storages.view_storage import ViewStorage


def get_list_views_resolver(root,info,params):
    list_view_storage = ListViewStorage()
    list_storage = ListStorage()
    view_storage = ViewStorage()
    list_permission_storage = ListPermissionStorage()

    interactor = ListViewInteractor(
        list_view_storage=list_view_storage,
        list_storage=list_storage,
        view_storage=view_storage,
        permission_storage=list_permission_storage
    )

    view_output = interactor.get_list_views(list_id=params.list_id)

    result =  [ListViewType(
                id=each.id,
                view_id=each.view_id,
                list_id=each.list_id,
                applied_by=each.applied_by,
                is_active=each.is_active
            )for each in view_output]

    return ListViewsType(list_views=result)
