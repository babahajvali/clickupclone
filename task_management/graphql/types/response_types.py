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
    DeletedTaskType, DeletedListType, DeletedSpaceType, \
    DeletedFolderType, ViewTypeNotFoundType, DeletedWorkspaceType, \
    UserNotWorkspaceOwnerType, UnexpectedRoleType, EmailNotFound, \
    IncorrectPassword, InactiveWorkspaceMemberType, \
    InvalidOrderType, UnsupportedVisibilityType, InvalidOffset, \
    InvalidLimitType, TaskAssigneeNotFoundType, ListViewNotFound, \
    InvalidResetToken, ResetTokenExpired, InvalidFieldValue, \
    EmptyAccountNameExistsType, NothingToUpdateAccountType, \
    InvalidAccountIdsType, UserHaveAlreadyListPermissionType, \
    NothingToUpdateFieldType, EmptyFieldNameType, MissingFieldConfigType, \
    DropdownOptionsMissingType, UserNotWorkspaceMemberType, DeletedFieldType, \
    EmptyFolderNameType, NothingToUpdateFolderType, EmptyListNameType, \
    EmptySpaceNameType, EmptyTaskTitleType, NothingToUpdateTaskType, \
    EmptyViewNameType, NothingToUpdateViewType, EmptyWorkspaceNameType, \
    InvalidWorkspaceIdsFoundType, WorkspaceMemberIdNotFoundType
from task_management.graphql.types.types import AccountType, UserType, \
    FieldType, TaskType, ListType, ViewType, FolderType, \
    SpaceType, WorkspaceType, WorkspaceMemberType, UserSpacePermissionType, \
    UserFolderPermissionType, UserListPermissionType, \
    WorkspaceSpacesType, SpaceFoldersType, ListsType, TasksType, \
    TaskAssigneeType, TaskAssigneesType, ViewsType, FieldsType, ListViewType, \
    ListViewsType, WorkspaceMembersType, TasksValuesType, FieldValueType, \
    WorkspaceUsersType, GetUserTaskType, \
    PasswordResetResponseType, AccountsType, ValidateResetTokenType, \
    WorkspacesType, TaskDetailsType


class CreateAccountResponse(graphene.Union):
    class Meta:
        types = (
            AccountType,
            AccountNameAlreadyExistsType,
            EmptyAccountNameExistsType,
            UserNotFoundType,
            InactiveUserType,
        )


class UpdateAccountResponse(graphene.Union):
    class Meta:
        types = (
            AccountType,
            AccountNotFoundType,
            InactiveAccountType,
            UserNotAccountOwnerType,
            AccountNameAlreadyExistsType,
            NothingToUpdateAccountType,
            EmptyAccountNameExistsType
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
            InvalidFieldDefaultValueType,
            ModificationNotAllowedType,
            EmptyFieldNameType,
            MissingFieldConfigType,
            DropdownOptionsMissingType
        )


class UpdateFieldResponse(graphene.Union):
    class Meta:
        types = (
            FieldType,
            FieldNotFoundType,
            ModificationNotAllowedType,
            InvalidFieldConfigType,
            InvalidFieldDefaultValueType,
            NothingToUpdateFieldType,
            FieldNameAlreadyExistsType,
            DeletedFieldType,
            EmptyFieldNameType,
            MissingFieldConfigType,
            DropdownOptionsMissingType,
            UserNotWorkspaceMemberType
        )


class CreateTaskResponse(graphene.Union):
    class Meta:
        types = (
            TaskType,
            ListNotFoundType,
            DeletedListType,
            ModificationNotAllowedType,
            EmptyTaskTitleType,
            UserNotWorkspaceMemberType,
        )


class UpdateTaskResponse(graphene.Union):
    class Meta:
        types = (
            TaskType,
            TaskNotFoundType,
            DeletedTaskType,
            ModificationNotAllowedType,
            NothingToUpdateTaskType,
            UserNotWorkspaceMemberType,
        )


class CreateListResponse(graphene.Union):
    class Meta:
        types = (
            ListType,
            SpaceNotFoundType,
            DeletedSpaceType,
            FolderNotFoundType,
            DeletedFolderType,
            ModificationNotAllowedType,
            EmptyListNameType,
            UserNotWorkspaceMemberType
        )


class UpdateListResponse(graphene.Union):
    class Meta:
        types = (
            ListType,
            ListNotFoundType,
            DeletedListType
        )


class CreateViewResponse(graphene.Union):
    class Meta:
        types = (
            ViewType,
            ViewTypeNotFoundType,
            EmptyViewNameType
        )


class UpdateViewResponse(graphene.Union):
    class Meta:
        types = (
            ViewType,
            ViewNotFoundType,
            NothingToUpdateViewType
        )


class CreateFolderResponse(graphene.Union):
    class Meta:
        types = (
            FolderType,
            SpaceNotFoundType,
            DeletedSpaceType,
            UserNotWorkspaceMemberType,
            EmptyFolderNameType
        )


class UpdateFolderResponse(graphene.Union):
    class Meta:
        types = (
            FolderType,
            FolderNotFoundType,
            DeletedFolderType,
            UserNotWorkspaceMemberType,
            NothingToUpdateFolderType,
        )


class CreateSpaceResponse(graphene.Union):
    class Meta:
        types = (
            SpaceType,
            WorkspaceNotFoundType,
            DeletedWorkspaceType,
            EmptySpaceNameType,
            UserNotWorkspaceMemberType
        )


class UpdateSpaceResponse(graphene.Union):
    class Meta:
        types = (
            SpaceType,
            SpaceNotFoundType,
            DeletedSpaceType
        )


class CreateWorkspaceResponse(graphene.Union):
    class Meta:
        types = (
            WorkspaceType,
            AccountNotFoundType,
            InactiveAccountType,
            UserNotAccountOwnerType,
            EmptyWorkspaceNameType,
            ModificationNotAllowedType
        )


class UpdateWorkspaceResponse(graphene.Union):
    class Meta:
        types = (
            WorkspaceType,
            WorkspaceNotFoundType,
            DeletedWorkspaceType,
            UserNotWorkspaceOwnerType,
        )


class DeleteWorkspaceResponse(graphene.Union):
    class Meta:
        types = (
            WorkspaceType,
            WorkspaceNotFoundType,
            UserNotWorkspaceOwnerType
        )


class TransferWorkspaceResponse(graphene.Union):
    class Meta:
        types = (
            WorkspaceType,
            WorkspaceNotFoundType,
            UserNotWorkspaceOwnerType,
            UserNotFoundType,
            InactiveUserType,
            DeletedWorkspaceType
        )


class GetWorkspaceResponse(graphene.Union):
    class Meta:
        types = (
            WorkspacesType,
            InvalidWorkspaceIdsFoundType
        )


class AddMemberToWorkspaceResponse(graphene.Union):
    class Meta:
        types = (
            WorkspaceMemberType,
            WorkspaceNotFoundType,
            DeletedWorkspaceType,
            UserNotFoundType,
            InactiveUserType,
            UnexpectedRoleType,
            ModificationNotAllowedType,
            UserNotWorkspaceMemberType
        )


class ChangeWorkspaceMemberRoleResponse(graphene.Union):
    class Meta:
        types = (
            WorkspaceMemberType,
            WorkspaceNotFoundType,
            DeletedWorkspaceType,
            UserNotFoundType,
            InactiveUserType,
            UnexpectedRoleType,
            ModificationNotAllowedType,
            UserNotWorkspaceMemberType
        )


class RemoveWorkspaceMemberResponse(graphene.Union):
    class Meta:
        types = (
            WorkspaceMemberType,
            UserNotWorkspaceMemberType,
            WorkspaceMemberIdNotFoundType,
            ModificationNotAllowedType,
            InactiveWorkspaceMemberType,
        )

class CreateUserSpacePermissionResponse(graphene.Union):
    class Meta:
        types = (
            UserSpacePermissionType,
            SpaceNotFoundType,
            DeletedSpaceType,
            UserNotFoundType,
            InactiveUserType,
            InactiveWorkspaceMemberType
        )


class CreateUserFolderPermissionResponse(graphene.Union):
    class Meta:
        types = (
            UserFolderPermissionType,
            FolderNotFoundType,
            DeletedFolderType,
            UserNotFoundType,
            InactiveUserType,
            InactiveWorkspaceMemberType
        )


class CreateUserListPermissionResponse(graphene.Union):
    class Meta:
        types = (
            UserListPermissionType,
            ListNotFoundType,
            DeletedListType,
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
            UserNotAccountOwnerType
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
            UserNotWorkspaceMemberType,
            ModificationNotAllowedType
        )


class ReorderSpaceResponse(graphene.Union):
    class Meta:
        types = (
            SpaceType,
            WorkspaceNotFoundType,
            DeletedWorkspaceType,
            ModificationNotAllowedType,
            InvalidOrderType,
            SpaceNotFoundType,
            DeletedSpaceType,
            UserNotWorkspaceMemberType,
        )


class SetSpaceVisibilityResponse(graphene.Union):
    class Meta:
        types = (
            SpaceType,
            SpaceNotFoundType,
            DeletedSpaceType,
            ModificationNotAllowedType,
            UnsupportedVisibilityType,
            UserNotWorkspaceMemberType
        )


class ReorderFolderResponse(graphene.Union):
    class Meta:
        types = (
            FolderType,
            FolderNotFoundType,
            DeletedFolderType,
            ModificationNotAllowedType,
            InvalidOrderType,
            SpaceNotFoundType,
            DeletedSpaceType,
            UserNotWorkspaceMemberType
        )


class SetFolderVisibilityResponse(graphene.Union):
    class Meta:
        types = (
            FolderType,
            FolderNotFoundType,
            DeletedFolderType,
            ModificationNotAllowedType,
            UnsupportedVisibilityType,
            UserNotWorkspaceMemberType
        )


class GetSpaceFoldersResponse(graphene.Union):
    class Meta:
        types = (
            SpaceFoldersType,
            SpaceNotFoundType,
            DeletedSpaceType
        )


class GetUserFolderPermissionResponse(graphene.Union):
    class Meta:
        types = (
            UserFolderPermissionType,
            FolderNotFoundType,
            DeletedFolderType,
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
            ModificationNotAllowedType,
            UserNotWorkspaceMemberType
        )


class GetWorkspaceSpacesResponse(graphene.Union):
    class Meta:
        types = (
            WorkspaceSpacesType,
            WorkspaceNotFoundType,
            DeletedWorkspaceType
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
            ModificationNotAllowedType,
            UserNotWorkspaceMemberType
        )


class ReorderListInFolderResponse(graphene.Union):
    class Meta:
        types = (
            ListType,
            ListNotFoundType,
            DeletedListType,
            ModificationNotAllowedType,
            InvalidOrderType,
            UserNotWorkspaceMemberType,
            FolderNotFoundType,
            DeletedFolderType,
        )


class ReorderListInSpaceResponse(graphene.Union):
    class Meta:
        types = (
            ListType,
            ListNotFoundType,
            DeletedListType,
            ModificationNotAllowedType,
            InvalidOrderType,
            SpaceNotFoundType,
            DeletedSpaceType,
            UserNotWorkspaceMemberType,
        )


class SetListVisibilityResponse(graphene.Union):
    class Meta:
        types = (
            ListType,
            ListNotFoundType,
            DeletedListType,
            ModificationNotAllowedType,
            UnsupportedVisibilityType,
            UserNotWorkspaceMemberType
        )


class GetFolderListsResponse(graphene.Union):
    class Meta:
        types = (
            ListsType,
            FolderNotFoundType,
            DeletedFolderType
        )


class GetSpaceListsResponse(graphene.Union):
    class Meta:
        types = (
            ListsType,
            SpaceNotFoundType,
            DeletedSpaceType
        )


class GetListResponse(graphene.Union):
    class Meta:
        types = (
            ListType,
            ListNotFoundType,
        )


class DeleteTaskResponse(graphene.Union):
    class Meta:
        types = (
            TaskType,
            TaskNotFoundType,
            UserNotWorkspaceMemberType,
            ModificationNotAllowedType
        )


class ReorderTaskResponse(graphene.Union):
    class Meta:
        types = (
            TaskType,
            TaskNotFoundType,
            DeletedTaskType,
            ModificationNotAllowedType,
            InvalidOrderType,
            UserNotWorkspaceMemberType
        )


class GetListTasksResponse(graphene.Union):
    class Meta:
        types = (
            TaskDetailsType,
            ListNotFoundType,
            DeletedListType
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
            DeletedListType,
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
                 DeletedListType,
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
            InvalidOrderType,
            UserNotWorkspaceMemberType,
            DeletedFieldType
        )


class DeleteFieldResponse(graphene.Union):
    class Meta:
        types = (
            FieldType,
            FieldNotFoundType,
            ModificationNotAllowedType,
            UserNotWorkspaceMemberType
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
            DeletedListType,
            ModificationNotAllowedType,
            UserNotWorkspaceMemberType
        )


class RemoveListViewResponse(graphene.Union):
    class Meta:
        types = (
            ListViewType,
            ModificationNotAllowedType,
            ListViewNotFound,
            UserNotWorkspaceMemberType
        )


class GetListViewsResponse(graphene.Union):
    class Meta:
        types = (
            ListViewsType,
            ListNotFoundType,
            DeletedListType
        )


class GetUserWorkspacesResponse(graphene.Union):
    class Meta:
        types = (
            WorkspaceMembersType,
            UserNotFoundType,
            InactiveUserType
        )


class GetTaskFieldValuesResponse(graphene.Union):
    class Meta:
        types = (TasksValuesType,
                 )


class SetTaskFieldValueResponse(graphene.Union):
    class Meta:
        types = (FieldValueType,
                 TaskNotFoundType,
                 DeletedTaskType,
                 FieldNotFoundType,
                 DeletedFieldType,
                 UserNotWorkspaceMemberType,
                 ModificationNotAllowedType,
                 InvalidFieldValue)


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


class GetAccountsResponse(graphene.Union):
    class Meta:
        types = (AccountsType,
                 InvalidAccountIdsType,)


class GetUserAccountsResponse(graphene.Union):
    class Meta:
        types = (
            AccountsType,
        )


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


class AddListPermissionForUserResponse(graphene.Union):
    class Meta:
        types = (UserListPermissionType,
                 DeletedListType,
                 UserHaveAlreadyListPermissionType,
                 ModificationNotAllowedType)
