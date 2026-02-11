import graphene


class UserNotFoundType(graphene.ObjectType):
    user_id = graphene.String(required=True)


class InactiveUserType(graphene.ObjectType):
    user_id = graphene.String(required=True)


class TemplateNotFoundType(graphene.ObjectType):
    template_id = graphene.String(required=True)


class UnsupportedFieldTypeType(graphene.ObjectType):
    field_type = graphene.String(required=True)


class FieldNameAlreadyExistsType(graphene.ObjectType):
    field_name = graphene.String(required=True)


class ModificationNotAllowedType(graphene.ObjectType):
    user_id = graphene.String(required=True)


class InvalidFieldValue(graphene.ObjectType):
    message = graphene.String(required=True)


class UnsupportedVisibilityType(graphene.ObjectType):
    visibility = graphene.String(required=True)


class FieldNotFoundType(graphene.ObjectType):
    field_id = graphene.String(required=True)


class InvalidFieldConfigType(graphene.ObjectType):
    field_type = graphene.String(required=True)
    invalid_keys = graphene.List(graphene.String)
    message = graphene.String()


class InvalidFieldDefaultValueType(graphene.ObjectType):
    field_type = graphene.String(required=True)
    default_value = graphene.String()
    message = graphene.String()


class TemplateNameAlreadyExistsType(graphene.ObjectType):
    template_name = graphene.String(required=True)


class ListNotFoundType(graphene.ObjectType):
    list_id = graphene.String(required=True)


class TaskNotFoundType(graphene.ObjectType):
    task_id = graphene.String(required=True)


class TaskAssigneeNotFoundType(graphene.ObjectType):
    assign_id = graphene.String(required=True)


class DeletedTaskType(graphene.ObjectType):
    task_id = graphene.String(required=True)


class InactiveListType(graphene.ObjectType):
    list_id = graphene.String(required=True)


class SpaceNotFoundType(graphene.ObjectType):
    space_id = graphene.String(required=True)


class InactiveSpaceType(graphene.ObjectType):
    space_id = graphene.String(required=True)


class FolderNotFoundType(graphene.ObjectType):
    folder_id = graphene.String()


class InactiveFolderType(graphene.ObjectType):
    folder_id = graphene.String()


class ViewTypeNotFoundType(graphene.ObjectType):
    view_type = graphene.String(required=True)


class ViewNotFoundType(graphene.ObjectType):
    view_id = graphene.String(required=True)


class WorkspaceNotFoundType(graphene.ObjectType):
    workspace_id = graphene.String(required=True)


class InactiveWorkspaceType(graphene.ObjectType):
    workspace_id = graphene.String(required=True)


class UserNotWorkspaceOwnerType(graphene.ObjectType):
    user_id = graphene.String(required=True)


class UnexpectedRoleType(graphene.ObjectType):
    role = graphene.String(required=True)


class UserDoesNotHaveListPermissionType(graphene.ObjectType):
    user_id = graphene.String(required=True)


class EmailNotFound(graphene.ObjectType):
    email = graphene.String(required=True)


class IncorrectPassword(graphene.ObjectType):
    password = graphene.String(required=True)


class UsernameAlreadyExists(graphene.ObjectType):
    username = graphene.String(required=True)


class EmailAlreadyExists(graphene.ObjectType):
    email = graphene.String(required=True)


class PhoneNumberAlreadyExists(graphene.ObjectType):
    phone_number = graphene.String(required=True)


class InvalidOffset(graphene.ObjectType):
    offset = graphene.Int(required=True)


class InvalidLimitType(graphene.ObjectType):
    limit = graphene.Int(required=True)


class InvalidOrderType(graphene.ObjectType):
    order = graphene.Int(required=True)


class InactiveWorkspaceMemberType(graphene.ObjectType):
    workspace_member_id = graphene.Int(required=True)


class AccountNameAlreadyExistsType(graphene.ObjectType):
    name = graphene.String(required=True)


class EmptyAccountNameExistsType(graphene.ObjectType):
    name = graphene.String(required=True)

class AccountNotFoundType(graphene.ObjectType):
    account_id = graphene.String(required=True)


class InactiveAccountType(graphene.ObjectType):
    account_id = graphene.String(required=True)


class UserNotAccountOwnerType(graphene.ObjectType):
    user_id = graphene.String(required=True)


class UserDoesNotHaveAccountPermissionType(graphene.ObjectType):
    user_id = graphene.String(required=True)


class ListViewNotFound(graphene.ObjectType):
    list_id = graphene.String(required=True)
    view_id = graphene.String(required=True)


class AccountMemberNotFoundType(graphene.ObjectType):
    account_member_id = graphene.Int(required=True)


class InvalidResetToken(graphene.ObjectType):
    token = graphene.String(required=True)


class ResetTokenExpired(graphene.ObjectType):
    token = graphene.String(required=True)


class InvalidAccountIds(graphene.ObjectType):
    account_ids = graphene.List(graphene.String, required=True)
