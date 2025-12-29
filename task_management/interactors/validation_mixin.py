from abc import abstractmethod

from task_management.exceptions.custom_exceptions import UserNotFoundException, \
    TemplateNotFoundException, UnexpectedFieldTypeFoundException, \
    FieldNameAlreadyExistsException, FieldOrderAlreadyExistsException, \
    NotAccessToCreateFieldException, FieldNotFoundException
from task_management.interactors.dtos import FieldTypeEnum, PermissionsEnum
from task_management.interactors.storage_interface.field_storage_interface import \
    FieldStorageInterface
from task_management.interactors.storage_interface.permission_storage_interface import \
    PermissionStorageInterface
from task_management.interactors.storage_interface.template_storage_interface import \
    TemplateStorageInterface
from task_management.interactors.storage_interface.user_storage_interface import \
    UserStorageInterface


class ValidationMixin:

    @staticmethod
    def check_user_exist(user_id: str, user_storage: UserStorageInterface):
        is_exist = user_storage.check_user_exist(user_id=user_id)

        if not is_exist:
            raise UserNotFoundException(user_id=user_id)


    @staticmethod
    def check_template_exist(template_id: str, template_storage: TemplateStorageInterface):
        is_exist = template_storage.check_template_exist(template_id=template_id)

        if not is_exist:
            raise TemplateNotFoundException(template_id=template_id)


    @staticmethod
    def check_field_type(field_type: str):

        field_types = [x.value for x in FieldTypeEnum]

        if field_type not in field_types:
            raise UnexpectedFieldTypeFoundException(field_type=field_type)


    @staticmethod
    def check_already_existed_field_name(field_name: str,template_id: str, field_storage: FieldStorageInterface):
        is_exist = field_storage.check_field_name_exist(field_name=field_name,template_id=template_id)

        if is_exist:
            raise FieldNameAlreadyExistsException(field_name=field_name)

    @staticmethod
    def check_field_order_is_valid(field_order: int, template_id: str, field_storage: FieldStorageInterface):

        is_exist = field_storage.check_field_order_exist(field_order=field_order,template_id=template_id)

        if is_exist:
            raise FieldOrderAlreadyExistsException(field_order=field_order)

    @staticmethod
    def check_user_has_access_to_create_field(user_id: str, permission_storage: PermissionStorageInterface):

        is_user_permissions = permission_storage.get_user_access_permissions(user_id=user_id)


        if is_user_permissions != PermissionsEnum.GUEST:
            raise NotAccessToCreateFieldException(user_id=user_id)

    @staticmethod
    def validate_field(field_id: str,template_id: str, field_storage: FieldStorageInterface):
        is_exist = field_storage.check_field_exist(field_id=field_id,template_id=template_id)

        if not is_exist:
            raise FieldNotFoundException(field_id=field_id)



