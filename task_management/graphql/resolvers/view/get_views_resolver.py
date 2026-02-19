from task_management.graphql.types.types import ViewType, ViewsType
from task_management.interactors.view.view_interactor import \
    ViewInteractor
from task_management.storages import ViewStorage, ListStorage


def get_all_views_resolver(root, info):
    view_storage = ViewStorage()
    list_storage = ListStorage()

    interactor = ViewInteractor(
        view_storage=view_storage,
        list_storage=list_storage
    )

    views_data = interactor.get_views()

    views_output = [
        ViewType(
            view_id=view.view_id,
            name=view.name,
            description=view.description,
            view_type=view.view_type.value,
            created_by=view.created_by_user_id
        ) for view in views_data
    ]

    return ViewsType(views=views_output)