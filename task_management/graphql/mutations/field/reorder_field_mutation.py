import graphene

from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import FieldNotFoundType, \
    TemplateNotFoundType, ModificationNotAllowedType, InvalidOrderType
from task_management.graphql.types.input_types import ReorderFieldInputParams
from task_management.graphql.types.response_types import ReorderFieldResponse
from task_management.graphql.types.types import FieldType
from task_management.interactors.field_interactors.field_interactors import \
    FieldInteractor
from task_management.storages.field_storage import FieldStorage
from task_management.storages.list_storage import ListStorage
from task_management.storages.template_storage import TemplateStorage
from task_management.storages.list_permission_storage import \
    ListPermissionStorage


class ReorderFieldMutation(graphene.Mutation):
    class Arguments:
        params = ReorderFieldInputParams(required=True)

    Output = ReorderFieldResponse

    @staticmethod
    def mutate(root, info, params):
        field_storage = FieldStorage()
        template_storage = TemplateStorage()
        permission_storage = ListPermissionStorage()
        list_storage = ListStorage()

        interactor = FieldInteractor(
            field_storage=field_storage,
            template_storage=template_storage,
            permission_storage=permission_storage,
            list_storage=list_storage
        )

        try:
            result = interactor.reorder_field(
                field_id=params.field_id,
                template_id=params.template_id,
                new_order=params.new_order,
                user_id=info.context.user_id
            )

            return FieldType(
                field_id=result.field_id,
                field_type=result.field_type.value,
                description=result.description,
                template_id=result.template_id,
                field_name=result.field_name,
                is_active=result.is_active,
                order=result.order,
                config=result.config,
                is_required=result.is_required,
                created_by=result.created_by
            )

        except custom_exceptions.FieldNotFoundException as e:
            return FieldNotFoundType(field_id=e.field_id)

        except custom_exceptions.TemplateNotFoundException as e:
            return TemplateNotFoundType(template_id=e.template_id)

        except custom_exceptions.ModificationNotAllowedException as e:
            return ModificationNotAllowedType(user_id=e.user_id)

        except custom_exceptions.InvalidOrderException as e:
            return InvalidOrderType(order=e.order)
