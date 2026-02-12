from task_management.graphql.types.types import ListViewType, ListViewsType
from task_management.interactors.view.list_view_interactor import \
    ListViewInteractor
from task_management.storages.list_storage import ListStorage
from task_management.storages.list_view_storage import ListViewStorage
from task_management.storages.space_storage import SpaceStorage
from task_management.storages.view_storage import ViewStorage
from task_management.storages.workspace_storage import WorkspaceStorage


def get_list_views_resolver(root,info,params):
    list_view_storage = ListViewStorage()
    list_storage = ListStorage()
    view_storage = ViewStorage()
    workspace_storage = WorkspaceStorage()
    space_storage = SpaceStorage()

    interactor = ListViewInteractor(
        list_view_storage=list_view_storage,
        list_storage=list_storage,
        view_storage=view_storage,
        workspace_storage=workspace_storage,
        space_storage=space_storage,
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
