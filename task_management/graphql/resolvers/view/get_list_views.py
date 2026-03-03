from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import ListNotFoundType, \
    DeletedListType
from task_management.graphql.types.types import ListViewType, ListViewsType
from task_management.interactors.views.get_list_views_interactor import \
    GetListViewsInteractor
from task_management.storages import ListStorage, ViewStorage


def get_list_views_resolver(root, info, params):
    list_storage = ListStorage()
    view_storage = ViewStorage()

    interactor = GetListViewsInteractor(
        list_storage=list_storage,
        view_storage=view_storage,
    )

    view_output = interactor.get_list_views(list_id=params.list_id)

    try:

        result = [ListViewType(
            id=each.id,
            view_id=each.view_id,
            list_id=each.list_id,
            applied_by=each.applied_by,
            is_active=each.is_active
        ) for each in view_output]

        return ListViewsType(list_views=result)

    except custom_exceptions.ListNotFound as e:
        return ListNotFoundType(list_id=e.list_id)

    except custom_exceptions.DeletedListFound as e:
        return DeletedListType(list_id=e.list_id)
