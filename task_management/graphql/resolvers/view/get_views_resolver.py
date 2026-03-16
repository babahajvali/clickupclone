from task_management.exceptions.enums import ViewType
from task_management.graphql.types.types import ViewsType


def get_all_views_resolver(root, info):
    views_output = ViewType.get_values()

    return ViewsType(views=views_output)
