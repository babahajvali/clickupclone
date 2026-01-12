import graphene

from django.core.exceptions import ObjectDoesNotExist
from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import ViewNotFoundType
from task_management.graphql.types.input_types import UpdateViewInputParams
from task_management.graphql.types.response_types import UpdateViewResponse
from task_management.graphql.types.types import ViewType
from task_management.interactors.view_interactors.view_interactors import \
    ViewInteractor
from task_management.interactors.dtos import UpdateViewDTO
from task_management.storages.view_storage import ViewStorage
from task_management.storages.list_permission_storage import ListPermissionStorage
from task_management.storages.list_storage import ListStorage


class UpdateViewMutation(graphene.Mutation):
    class Arguments:
        params = UpdateViewInputParams(required=True)

    Output = UpdateViewResponse

    @staticmethod
    def mutate(root, info, params):
        view_storage = ViewStorage()
        permission_storage = ListPermissionStorage()
        list_storage = ListStorage()

        interactor = ViewInteractor(
            view_storage=view_storage,
            permission_storage=permission_storage,
            list_storage=list_storage
        )

        try:
            update_view_data = UpdateViewDTO(
                view_id=params.view_id,
                name=params.name if params.name else None,
                description=params.description if params.description else None
            )

            result = interactor.update_view(update_view_data=update_view_data)

            return ViewType(
                view_id=str(result.view_id),
                name=result.name,
                description=result.description,
                view_type=result.view_type.value if hasattr(result.view_type, 'value') else result.view_type,
                created_by=str(result.created_by)
            )

        except custom_exceptions.ViewNotFoundException as e:
            return ViewNotFoundType(view_id=e.view_id)

        except ObjectDoesNotExist:
            return ViewNotFoundType(view_id=params.view_id)