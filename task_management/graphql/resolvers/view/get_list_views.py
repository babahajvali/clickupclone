from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import ListNotFoundType, \
    DeletedListType
from task_management.graphql.types.types import ListViewType, ListViewsType
from task_management.interactors.views.get_list_views_interactor import \
    GetListViewsInteractor
from task_management.storages import ListStorage, ListViewStorage


def get_list_views_resolver(root, info, params):
    list_storage = ListStorage()
    view_storage = ListViewStorage()

    interactor = GetListViewsInteractor(
        list_storage=list_storage,
        view_storage=view_storage,
    )

    try:
        view_output = interactor.get_list_views(list_id=params.list_id)

        result = [ListViewType(
            id=each.id,
            view_name=each.view_name,
            view_type=each.view_type,
            list_id=each.list_id,
            created_by=each.created_by,
            is_active=each.is_active
        ) for each in view_output]

        return ListViewsType(list_views=result)

    except custom_exceptions.ListNotFound as e:
        return ListNotFoundType(list_id=e.list_id)

    except custom_exceptions.ListIsDeleted as e:
        return DeletedListType(list_id=e.list_id)
