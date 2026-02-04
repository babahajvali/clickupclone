import graphene

from task_management.graphql.types.error_types import \
    AccountNameAlreadyExistsType, UsernameAlreadyExists, \
    EmailAlreadyExists, PhoneNumberAlreadyExists, \
    UserNotFoundType, AccountNotFoundType, InactiveUserType, \
    InactiveAccountType, UserNotAccountOwnerType, FieldNotFoundType, \
    TemplateNotFoundType, TaskNotFoundType, ListNotFoundType, \
    ViewNotFoundType, FolderNotFoundType, SpaceNotFoundType, \
    WorkspaceNotFoundType, UnsupportedFieldTypeType, \
    FieldNameAlreadyExistsType, ModificationNotAllowedType, \
    InvalidFieldConfigType, InvalidFieldDefaultValueType, \
    DeletedTaskType, InactiveListType, InactiveSpaceType, \
    InactiveFolderType, ViewTypeNotFoundType, InactiveWorkspaceType, \
    UserNotWorkspaceOwnerType, UnexpectedRoleType, EmailNotFound, \
    IncorrectPassword, InactiveWorkspaceMemberType, \
    InvalidOrderType, UnsupportedVisibilityType, InvalidOffset, \
    InvalidLimitType, TaskAssigneeNotFoundType, ListViewNotFound, \
    InvalidResetToken, \
    ResetTokenExpired, InvalidAccountIds
from task_management.graphql.types.types import AccountType, UserType, \
    FieldType, TaskType, ListType, ViewType, FolderType, \
    SpaceType, WorkspaceType, WorkspaceMemberType, UserSpacePermissionType, \
    UserFolderPermissionType, UserListPermissionType, \
    WorkspaceSpacesType, SpaceFoldersType, ListsType, TasksType, \
    TaskAssigneeType, TaskAssigneesType, ViewsType, FieldsType, ListViewType, \
    ListViewsType, WorkspaceMembersType, TasksValuesType, TaskFieldValuesType, \
    FieldValueType, WorkspaceUsersType, GetUserTaskType, \
    PasswordResetResponseType, AccountsType, ValidateResetTokenType


class CreateAccountResponse(graphene.Union):
    class Meta:
        types = (
            AccountType,
            AccountNameAlreadyExistsType
        )


class UpdateAccountResponse(graphene.Union):
    class Meta:
        types = (
            AccountType,
            AccountNotFoundType,
            InactiveAccountType,
            UserNotAccountOwnerType,
            AccountNameAlreadyExistsType
        )


class CreateUserResponse(graphene.Union):
    class Meta:
        types = (
            UserType,
            UsernameAlreadyExists,
            EmailAlreadyExists,
            PhoneNumberAlreadyExists,
        )


class UpdateUserResponse(graphene.Union):
    class Meta:
        types = (
            UserType,
            UserNotFoundType,
            InactiveUserType,
            UsernameAlreadyExists,
            EmailAlreadyExists,
            PhoneNumberAlreadyExists,
        )


class CreateFieldResponse(graphene.Union):
    class Meta:
        types = (
            FieldType,
            TemplateNotFoundType,
            UnsupportedFieldTypeType,
            FieldNameAlreadyExistsType,
            InvalidFieldConfigType,
            InvalidFieldDefaultValueType
        )


class UpdateFieldResponse(graphene.Union):
    class Meta:
        types = (
            FieldType,
            FieldNotFoundType,
            ModificationNotAllowedType,
            InvalidFieldConfigType,
            InvalidFieldDefaultValueType
        )


class CreateTaskResponse(graphene.Union):
    class Meta:
        types = (
            TaskType,
            ListNotFoundType,
            InactiveListType,
            ModificationNotAllowedType
        )


class UpdateTaskResponse(graphene.Union):
    class Meta:
        types = (
            TaskType,
            TaskNotFoundType,
            DeletedTaskType,
            InactiveListType,
            ListNotFoundType,
            ModificationNotAllowedType
        )


class CreateListResponse(graphene.Union):
    class Meta:
        types = (
            ListType,
            SpaceNotFoundType,
            InactiveSpaceType,
            FolderNotFoundType,
            InactiveFolderType,
            ModificationNotAllowedType
        )


class UpdateListResponse(graphene.Union):
    class Meta:
        types = (
            ListType,
            ListNotFoundType,
            InactiveListType
        )


class CreateViewResponse(graphene.Union):
    class Meta:
        types = (
            ViewType,
            ViewTypeNotFoundType
        )


class UpdateViewResponse(graphene.Union):
    class Meta:
        types = (
            ViewType,
            ViewNotFoundType
        )


class CreateFolderResponse(graphene.Union):
    class Meta:
        types = (
            FolderType,
            SpaceNotFoundType,
            InactiveSpaceType
        )


class UpdateFolderResponse(graphene.Union):
    class Meta:
        types = (
            FolderType,
            FolderNotFoundType,
            InactiveFolderType
        )


class CreateSpaceResponse(graphene.Union):
    class Meta:
        types = (
            SpaceType,
            WorkspaceNotFoundType,
            InactiveWorkspaceType
        )


class UpdateSpaceResponse(graphene.Union):
    class Meta:
        types = (
            SpaceType,
            SpaceNotFoundType,
            InactiveSpaceType
        )


class CreateWorkspaceResponse(graphene.Union):
    class Meta:
        types = (
            WorkspaceType,
            AccountNotFoundType,
            InactiveAccountType,
            UserNotFoundType,
            InactiveUserType,
            ModificationNotAllowedType
        )


class UpdateWorkspaceResponse(graphene.Union):
    class Meta:
        types = (
            WorkspaceType,
            WorkspaceNotFoundType,
            InactiveWorkspaceType,
            UserNotWorkspaceOwnerType,
            ModificationNotAllowedType
        )


class DeleteWorkspaceResponse(graphene.Union):
    class Meta:
        types = (
            WorkspaceType,
            WorkspaceNotFoundType,
            InactiveWorkspaceType,
            ModificationNotAllowedType
        )


class TransferWorkspaceResponse(graphene.Union):
    class Meta:
        types = (
            WorkspaceType,
            WorkspaceNotFoundType,
            UserNotWorkspaceOwnerType,
            UserNotFoundType,
            InactiveUserType
        )


class GetWorkspaceResponse(graphene.Union):
    class Meta:
        types = (
            WorkspaceType,
            WorkspaceNotFoundType
        )


class AddMemberToWorkspaceResponse(graphene.Union):
    class Meta:
        types = (
            WorkspaceMemberType,
            WorkspaceNotFoundType,
            InactiveWorkspaceType,
            UserNotFoundType,
            InactiveUserType,
            UnexpectedRoleType,
            ModificationNotAllowedType
        )


class CreateUserSpacePermissionResponse(graphene.Union):
    class Meta:
        types = (
            UserSpacePermissionType,
            SpaceNotFoundType,
            InactiveSpaceType,
            UserNotFoundType,
            InactiveUserType,
            InactiveWorkspaceMemberType
        )


class CreateUserFolderPermissionResponse(graphene.Union):
    class Meta:
        types = (
            UserFolderPermissionType,
            FolderNotFoundType,
            InactiveFolderType,
            UserNotFoundType,
            InactiveUserType,
            InactiveWorkspaceMemberType
        )


class CreateUserListPermissionResponse(graphene.Union):
    class Meta:
        types = (
            UserListPermissionType,
            ListNotFoundType,
            InactiveListType,
            UserNotFoundType,
            InactiveUserType,
            InactiveWorkspaceMemberType
        )


class UserLoginResponse(graphene.Union):
    class Meta:
        types = (
            UserType,
            EmailNotFound,
            IncorrectPassword,
            InactiveUserType,
        )


class GetUserProfileResponse(graphene.Union):
    class Meta:
        types = (
            UserType,
            UserNotFoundType,
            InactiveUserType
        )


class TransferAccountResponse(graphene.Union):
    class Meta:
        types = (
            AccountType,
            AccountNotFoundType,
            InactiveAccountType,
            UserNotAccountOwnerType,
            UserNotFoundType,
            InactiveUserType
        )


class DeleteAccountResponse(graphene.Union):
    class Meta:
        types = (
            AccountType,
            AccountNotFoundType,
            InactiveAccountType,
            ModificationNotAllowedType
        )


class BlockUserResponse(graphene.Union):
    class Meta:
        types = (
            UserType,
            UserNotFoundType,
            InactiveUserType
        )


class DeleteSpaceResponse(graphene.Union):
    class Meta:
        types = (
            SpaceType,
            SpaceNotFoundType,
            InactiveSpaceType,
            ModificationNotAllowedType
        )


class ReorderSpaceResponse(graphene.Union):
    class Meta:
        types = (
            SpaceType,
            WorkspaceNotFoundType,
            InactiveWorkspaceType,
            ModificationNotAllowedType,
            InvalidOrderType
        )


class SetSpaceVisibilityResponse(graphene.Union):
    class Meta:
        types = (
            SpaceType,
            SpaceNotFoundType,
            InactiveSpaceType,
            ModificationNotAllowedType,
            UnsupportedVisibilityType
        )


class ReorderFolderResponse(graphene.Union):
    class Meta:
        types = (
            FolderType,
            FolderNotFoundType,
            InactiveFolderType,
            ModificationNotAllowedType,
            InvalidOrderType
        )


class SetFolderVisibilityResponse(graphene.Union):
    class Meta:
        types = (
            FolderType,
            FolderNotFoundType,
            InactiveFolderType,
            ModificationNotAllowedType,
            UnsupportedVisibilityType
        )


class GetSpaceFoldersResponse(graphene.Union):
    class Meta:
        types = (
            SpaceFoldersType,
            SpaceNotFoundType,
            InactiveSpaceType
        )


class GetUserFolderPermissionResponse(graphene.Union):
    class Meta:
        types = (
            UserFolderPermissionType,
            FolderNotFoundType,
            InactiveFolderType,
            ModificationNotAllowedType
        )


class GetFolderResponse(graphene.Union):
    class Meta:
        types = (
            FolderType,
            FolderNotFoundType
        )


class DeleteFolderResponse(graphene.Union):
    class Meta:
        types = (
            FolderType,
            FolderNotFoundType,
            InactiveFolderType,
            ModificationNotAllowedType
        )


class GetWorkspaceSpacesResponse(graphene.Union):
    class Meta:
        types = (
            WorkspaceSpacesType,
            WorkspaceNotFoundType,
            InactiveWorkspaceType
        )


class GetSpaceResponse(graphene.Union):
    class Meta:
        types = (
            SpaceType,
            SpaceNotFoundType
        )


class DeleteListResponse(graphene.Union):
    class Meta:
        types = (
            ListType,
            ListNotFoundType,
            InactiveListType,
            ModificationNotAllowedType
        )


class ReorderListInFolderResponse(graphene.Union):
    class Meta:
        types = (
            ListType,
            ListNotFoundType,
            InactiveListType,
            ModificationNotAllowedType,
            InvalidOrderType
        )


class ReorderListInSpaceResponse(graphene.Union):
    class Meta:
        types = (
            ListType,
            ListNotFoundType,
            InactiveListType,
            ModificationNotAllowedType,
            InvalidOrderType
        )


class SetListVisibilityResponse(graphene.Union):
    class Meta:
        types = (
            ListType,
            ListNotFoundType,
            InactiveListType,
            ModificationNotAllowedType,
            UnsupportedVisibilityType
        )


class GetFolderListsResponse(graphene.Union):
    class Meta:
        types = (
            ListsType,
            FolderNotFoundType,
            InactiveFolderType
        )


class GetSpaceListsResponse(graphene.Union):
    class Meta:
        types = (
            ListsType,
            SpaceNotFoundType,
            InactiveSpaceType
        )


class GetListResponse(graphene.Union):
    class Meta:
        types = (
            ListType,
            ListNotFoundType,
            InactiveListType
        )


class DeleteTaskResponse(graphene.Union):
    class Meta:
        types = (
            TaskType,
            TaskNotFoundType,
            DeletedTaskType,
            ModificationNotAllowedType
        )


class ReorderTaskResponse(graphene.Union):
    class Meta:
        types = (
            TaskType,
            TaskNotFoundType,
            DeletedTaskType,
            ModificationNotAllowedType,
            InvalidOrderType
        )


class GetListTasksResponse(graphene.Union):
    class Meta:
        types = (
            TasksType,
            ListNotFoundType,
            InactiveListType
        )


class GetTaskResponse(graphene.Union):
    class Meta:
        types = (
            TaskType,
            TaskNotFoundType,
            DeletedTaskType
        )


class TaskFilterResponse(graphene.Union):
    class Meta:
        types = (
            TasksType,
            ListNotFoundType,
            InactiveListType,
            InvalidOffset,
            InvalidLimitType
        )


class CreateTaskAssigneeResponse(graphene.Union):
    class Meta:
        types = (TaskAssigneeType,
                 UserNotFoundType,
                 TaskNotFoundType,
                 InactiveUserType,
                 DeletedTaskType,
                 ModificationNotAllowedType)


class RemoveTaskAssigneeResponse(graphene.Union):
    class Meta:
        types = (TaskAssigneeType,
                 TaskAssigneeNotFoundType,
                 ListNotFoundType,
                 InactiveListType,
                 ModificationNotAllowedType)


class GetTaskAssigneesResponse(graphene.Union):
    class Meta:
        types = (TaskAssigneesType,
                 DeletedTaskType,
                 TaskNotFoundType)


class GetViewsResponse(graphene.Union):
    class Meta:
        types = (
            ViewsType,
            ViewNotFoundType
        )


class ReorderFieldResponse(graphene.Union):
    class Meta:
        types = (
            FieldType,
            FieldNotFoundType,
            TemplateNotFoundType,
            ModificationNotAllowedType,
            InvalidOrderType
        )


class DeleteFieldResponse(graphene.Union):
    class Meta:
        types = (
            FieldType,
            FieldNotFoundType,
            TemplateNotFoundType,
            ModificationNotAllowedType
        )


class GetFieldsForTemplateResponse(graphene.Union):
    class Meta:
        types = (
            FieldsType,
            TemplateNotFoundType
        )


class GetFieldResponse(graphene.Union):
    class Meta:
        types = (
            FieldType,
            FieldNotFoundType
        )


class ApplyListViewResponse(graphene.Union):
    class Meta:
        types = (
            ListViewType,
            ListNotFoundType,
            ViewNotFoundType,
            InactiveListType,
            ModificationNotAllowedType
        )


class RemoveListViewResponse(graphene.Union):
    class Meta:
        types = (
            ListViewType,
            ListNotFoundType,
            ModificationNotAllowedType,
            ListViewNotFound,
            InactiveListType
        )


class GetListViewsResponse(graphene.Union):
    class Meta:
        types = (
            ListViewsType,
            ListNotFoundType,
            InactiveListType
        )


class GetUserWorkspacesResponse(graphene.Union):
    class Meta:
        types = (
            WorkspaceMembersType,
            UserNotFoundType
        )


class GetTaskFieldValuesResponse(graphene.Union):
    class Meta:
        types = (TasksValuesType,
                 )


class SetTaskFieldValueResponse(graphene.Union):
    class Meta:
        types = (FieldValueType,
                 ModificationNotAllowedType)


class GetWorkspaceUsersResponse(graphene.Union):
    class Meta:
        types = (WorkspaceUsersType,)


class GetUserTasksResponse(graphene.Union):
    class Meta:
        types = (GetUserTaskType,
                 InactiveUserType,
                 UserNotFoundType)


def _resolve_union_type(obj, info):
    return type(obj)


class ForgotPasswordResponse(graphene.Union):
    class Meta:
        types = (PasswordResetResponseType, EmailNotFound)

    resolve_type = staticmethod(_resolve_union_type)


class ResetPasswordResponse(graphene.Union):
    class Meta:
        types = (UserType, InvalidResetToken, ResetTokenExpired)

    resolve_type = staticmethod(_resolve_union_type)


class GetListTaskAssigneesResponse(graphene.Union):
    class Meta:
        types = (TaskAssigneesType,
                 InactiveListType,
                 ListNotFoundType)


class GetAccountsResponse(graphene.Union):
    class Meta:
        types = (AccountsType,)


class GetUserWithEmailResponse(graphene.Union):
    class Meta:
        types = (
            UserType,
        )


class ValidateResetTokenResponse(graphene.Union):
    class Meta:
        types = (
            ValidateResetTokenType,
            InvalidResetToken,
            ResetTokenExpired
        )
