from task_management.graphql.types.types import ListViewType, ListViewsType
from task_management.interactors.views.list_view_interactor import \
    ListViewInteractor
from task_management.storages import ListStorage, ViewStorage, WorkspaceStorage


def get_list_views_resolver(root,info,params):
    list_storage = ListStorage()
    view_storage = ViewStorage()
    workspace_storage = WorkspaceStorage()

    interactor = ListViewInteractor(
        list_storage=list_storage,
        view_storage=view_storage,
        workspace_storage=workspace_storage,
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
