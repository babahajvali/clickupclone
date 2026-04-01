from functools import wraps

from task_management.exceptions import custom_exceptions
from task_management.graphql.types import error_types


def handle_field_exceptions(exception_map):
    """Decorator that catches exceptions and returns mapped GraphQL error types."""

    def decorator(mutate_fn):
        @wraps(mutate_fn)
        def wrapper(*args, **kwargs):
            try:
                return mutate_fn(*args, **kwargs)
            except Exception as e:
                handler = exception_map.get(type(e))
                if handler:
                    return handler(e)
                raise

        return wrapper

    return decorator


_COMMON_EXCEPTIONS = {
    custom_exceptions.FieldNotFound:
        lambda e: error_types.FieldNotFoundType(field_id=e.field_id),
    custom_exceptions.FieldIsDeleted:
        lambda e: error_types.DeletedFieldType(field_id=e.field_id),
    custom_exceptions.ModificationNotAllowed:
        lambda e: error_types.ModificationNotAllowedType(user_id=e.user_id),
    custom_exceptions.ResourceLocked:
        lambda e: error_types.ResourceLockedType(message=e.message),
    custom_exceptions.UserNotWorkspaceMember:
        lambda e: error_types.UserNotWorkspaceMemberType(user_id=e.user_id),
    custom_exceptions.FieldNameAlreadyExists:
        lambda e: error_types.FieldNameAlreadyExistsType(
            field_name=e.field_name),
    custom_exceptions.EmptyFieldName:
        lambda e: error_types.EmptyFieldNameType(field_name=e.field_name),
}

_CONFIG_VALIDATION_EXCEPTIONS = {
    custom_exceptions.UnexpectedFieldConfigKeys:
        lambda e: error_types.InvalidFieldConfigType(
            field_type=e.field_type, invalid_keys=e.invalid_keys,
            message=e.message),
    custom_exceptions.TextDefaultValueExceedsMaxLength:
        lambda e: error_types.TextDefaultValueExceedsMaxLengthType(
            message=e.message),
    custom_exceptions.NumberDefaultValueBelowMinimum:
        lambda e: error_types.NumberDefaultValueBelowMinimumType(
            message=e.message),
    custom_exceptions.NumberValueBelowMinimum:
        lambda e: error_types.NumberDefaultValueBelowMinimumType(
            message=e.message),
    custom_exceptions.NumberDefaultValueAboveMaximum:
        lambda e: error_types.NumberDefaultValueAboveMaximumType(
            message=e.message),
    custom_exceptions.NumberValueExceedsMaximum:
        lambda e: error_types.NumberDefaultValueAboveMaximumType(
            message=e.message),
    custom_exceptions.DropdownDefaultValueNotInOptions:
        lambda e: error_types.DropdownDefaultValueNotInOptionsType(
            message=e.message),
    custom_exceptions.DuplicateDropdownOptions:
        lambda e: error_types.DuplicateDropdownOptionsType(
            message=e.message),
    custom_exceptions.EmptyDropdownConfig:
        lambda e: error_types.MissingFieldConfigType(
            field_type=e.field_type),
    custom_exceptions.DropdownOptionsEmpty:
        lambda e: error_types.DropdownOptionsMissingType(
            message=e.message),
    custom_exceptions.EmptyDropdownOptions:
        lambda e: error_types.EmptyDropdownOptionsType(
            message=e.message),
    custom_exceptions.MaxValueLessThanMinValue:
        lambda e: error_types.MaxValueLessThanMinValueType(
            field_type=e.field_type, message=e.message),
}

CREATE_FIELD_EXCEPTIONS = {
    **_COMMON_EXCEPTIONS,
    **_CONFIG_VALIDATION_EXCEPTIONS,
    custom_exceptions.TemplateNotFound:
        lambda e: error_types.TemplateNotFoundType(
            template_id=e.template_id),
    custom_exceptions.InvalidFieldType:
        lambda e: error_types.UnsupportedFieldTypeType(
            field_type=e.field_type),
}

UPDATE_FIELD_EXCEPTIONS = {
    **_COMMON_EXCEPTIONS,
    **_CONFIG_VALIDATION_EXCEPTIONS,
    custom_exceptions.NothingToUpdateField:
        lambda e: error_types.NothingToUpdateFieldType(field_id=e.field_id),
}

DELETE_FIELD_EXCEPTIONS = {
    custom_exceptions.FieldNotFound:
        lambda e: error_types.FieldNotFoundType(field_id=e.field_id),
    custom_exceptions.ModificationNotAllowed:
        lambda e: error_types.ModificationNotAllowedType(user_id=e.user_id),
    custom_exceptions.ResourceLocked:
        lambda e: error_types.ResourceLockedType(message=e.message),
    custom_exceptions.UserNotWorkspaceMember:
        lambda e: error_types.UserNotWorkspaceMemberType(user_id=e.user_id),
}

REORDER_FIELD_EXCEPTIONS = {
    custom_exceptions.FieldNotFound:
        lambda e: error_types.FieldNotFoundType(field_id=e.field_id),
    custom_exceptions.FieldIsDeleted:
        lambda e: error_types.DeletedFieldType(field_id=e.field_id),
    custom_exceptions.FieldNotBelongsToTemplate:
        lambda e: error_types.FieldNotBelongsToTemplateType(
            field_id=e.field_id, template_id=e.template_id),
    custom_exceptions.TemplateNotFound:
        lambda e: error_types.TemplateNotFoundType(
            template_id=e.template_id),
    custom_exceptions.ModificationNotAllowed:
        lambda e: error_types.ModificationNotAllowedType(user_id=e.user_id),
    custom_exceptions.ResourceLocked:
        lambda e: error_types.ResourceLockedType(message=e.message),
    custom_exceptions.InvalidOrder:
        lambda e: error_types.InvalidOrderType(order=e.order),
    custom_exceptions.UserNotWorkspaceMember:
        lambda e: error_types.UserNotWorkspaceMemberType(user_id=e.user_id),
}

SET_FIELD_VALUE_EXCEPTIONS = {
    custom_exceptions.TaskNotFound:
        lambda e: error_types.TaskNotFoundType(task_id=e.task_id),
    custom_exceptions.TaskIsDeleted:
        lambda e: error_types.DeletedTaskType(task_id=e.task_id),
    custom_exceptions.FieldNotFound:
        lambda e: error_types.FieldNotFoundType(field_id=e.field_id),
    custom_exceptions.FieldIsDeleted:
        lambda e: error_types.DeletedFieldType(field_id=e.field_id),
    custom_exceptions.UserNotWorkspaceMember:
        lambda e: error_types.UserNotWorkspaceMemberType(user_id=e.user_id),
    custom_exceptions.ModificationNotAllowed:
        lambda e: error_types.ModificationNotAllowedType(user_id=e.user_id),
    custom_exceptions.InvalidFieldValue:
        lambda e: error_types.InvalidFieldValue(message=e.message),
    custom_exceptions.TextValueExceedsMaxLength:
        lambda e: error_types.TextValueExceedsMaxLengthType(
            message=e.message),
    custom_exceptions.InvalidNumberFieldValue:
        lambda e: error_types.InvalidNumberFieldValueType(
            message=e.message),
    custom_exceptions.NumberValueBelowMinimum:
        lambda e: error_types.NumberValueBelowMinimumType(
            message=e.message),
    custom_exceptions.NumberValueExceedsMaximum:
        lambda e: error_types.NumberValueExceedsMaximumType(
            message=e.message),
    custom_exceptions.DropdownOptionNotAllowed:
        lambda e: error_types.DropdownOptionNotAllowedType(
            message=e.message),
}
