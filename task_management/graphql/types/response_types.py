import graphene

from task_management.graphql.types.error_types import \
    AccountNameAlreadyExistsType, ExistedUsernameFoundType, \
    ExistedEmailFoundType, ExistedPhoneNumberFoundType, \
    UserNotFoundType, AccountNotFoundType, InactiveUserType, \
    InactiveAccountType, UserNotAccountOwnerType, FieldNotFoundType, \
    TemplateNotFoundType, TaskNotFoundType, ListNotFoundType, \
    ViewNotFoundType, FolderNotFoundType, SpaceNotFoundType, \
    WorkspaceNotFoundType, UnsupportedFieldTypeType, \
    FieldNameAlreadyExistsType, ModificationNotAllowedType, \
    InvalidFieldConfigType, InvalidFieldDefaultValueType, \
    TemplateNameAlreadyExistsType, \
    DeletedTaskType, InactiveListType, InactiveSpaceType, \
    InactiveFolderType, ViewTypeNotFoundType, InactiveWorkspaceType, \
    UserNotWorkspaceOwnerType, UnexpectedRoleType, \
    UserDoesNotHaveListPermissionType, NotExistedEmailFoundType, \
    WrongPasswordFoundType, InactiveWorkspaceMemberType, \
     InvalidOrderType
from task_management.graphql.types.types import AccountType, UserType, \
    FieldType, TemplateType, TaskType, ListType, ViewType, FolderType, \
    SpaceType, WorkspaceType, WorkspaceMemberType, UserSpacePermissionType, \
    UserFolderPermissionType, UserListPermissionType, AccountMemberType, \
    WorkspaceSpacesType


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
            InactiveAccountType
        )


class CreateUserResponse(graphene.Union):
    class Meta:
        types = (
            UserType,
            ExistedUsernameFoundType,
            ExistedEmailFoundType,
            ExistedPhoneNumberFoundType,
        )


class UpdateUserResponse(graphene.Union):
    class Meta:
        types = (
            UserType,
            UserNotFoundType,
            InactiveUserType,
            ExistedUsernameFoundType,
            ExistedEmailFoundType,
            ExistedPhoneNumberFoundType,
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


class CreateTemplateResponse(graphene.Union):
    class Meta:
        types = (
            TemplateType,
            ListNotFoundType,
            InactiveListType,
            TemplateNameAlreadyExistsType
        )


class UpdateTemplateResponse(graphene.Union):
    class Meta:
        types = (
            TemplateType,
            TemplateNotFoundType,
            TemplateNameAlreadyExistsType
        )


class CreateTaskResponse(graphene.Union):
    class Meta:
        types = (
            TaskType,
            ListNotFoundType,
            InactiveListType,
            UserDoesNotHaveListPermissionType
        )


class UpdateTaskResponse(graphene.Union):
    class Meta:
        types = (
            TaskType,
            TaskNotFoundType,
            DeletedTaskType,
            UserDoesNotHaveListPermissionType
        )


class CreateListResponse(graphene.Union):
    class Meta:
        types = (
            ListType,
            SpaceNotFoundType,
            InactiveSpaceType,
            FolderNotFoundType,
            InactiveFolderType
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
            UnexpectedRoleType
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

class CreateAccountMemberResponse(graphene.Union):
    class Meta:
        types = (
            AccountMemberType,
            AccountNotFoundType,
            InactiveAccountType,
            UserNotFoundType,
            InactiveUserType,
            UnexpectedRoleType
        )


class UserLoginResponse(graphene.Union):
    class Meta:
        types = (
            UserType,
            NotExistedEmailFoundType,
            WrongPasswordFoundType
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