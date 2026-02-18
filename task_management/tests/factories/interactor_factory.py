import uuid

import factory

from task_management.exceptions.enums import FieldTypes, Role
from task_management.interactors.dtos import CreateFieldDTO, FieldDTO, \
    CreateTemplateDTO, TemplateDTO, CreateListDTO, \
    UpdateListDTO, ListDTO, CreateTaskDTO, UpdateTaskDTO, TaskDTO, \
    TaskAssigneeDTO, UserTasksDTO, CreateFolderDTO, UpdateFolderDTO, \
    CreateViewDTO, UpdateViewDTO, ViewDTO, ListViewDTO, RemoveListViewDTO, \
    CreateSpaceDTO, SpaceDTO, CreateWorkspaceDTO, WorkspaceDTO, \
    AddMemberToWorkspaceDTO, WorkspaceMemberDTO, CreateAccountDTO, AccountDTO, \
    CreateAccountMemberDTO, AccountMemberDTO, FolderDTO


class CreateFieldFactory(factory.Factory):
    class Meta:
        model = CreateFieldDTO

    template_id = factory.Faker("uuid4")
    field_name = factory.Faker("name")
    description = factory.Faker("text")
    field_type = factory.Iterator([x.value for x in FieldTypes])
    is_required = factory.Faker("boolean")
    created_by = factory.Faker("uuid4")
    config = factory.LazyAttribute(lambda o: {
        "options": ["Option 1",
                    "Option 2"] if o.field_type == FieldTypes.DROPDOWN.value else {}
    })


class FieldDTOFactory(factory.Factory):
    class Meta:
        model = FieldDTO

    field_id = factory.Faker("uuid4")
    template_id = factory.Faker("uuid4")
    field_name = factory.Faker("name")
    description = factory.Faker("text")
    is_active = factory.Faker("boolean")
    field_type = factory.Iterator([x.value for x in FieldTypes])
    order = factory.sequence(lambda n: n + 1)
    config = factory.LazyFunction(dict)
    is_required = factory.Faker("boolean")
    created_by = factory.Faker("uuid4")


class CreateTemplateDTOFactory(factory.Factory):
    class Meta:
        model = CreateTemplateDTO

    name = factory.Faker("word")
    description = factory.Faker("sentence")
    list_id = factory.Faker("uuid4")
    created_by = factory.Faker("uuid4")



class TemplateDTOFactory(factory.Factory):
    class Meta:
        model = TemplateDTO

    template_id = factory.Faker("uuid4")
    name = factory.Faker("word")
    list_id = factory.Faker("uuid4")
    description = factory.Faker("sentence")
    created_by = factory.Faker("uuid4")


class CreateListDTOFactory(factory.Factory):
    class Meta:
        model = CreateListDTO

    name = factory.Faker("word")
    description = factory.Faker("sentence")
    space_id = factory.Faker("uuid4")
    is_private = False
    created_by = factory.Faker("uuid4")
    folder_id = None


class UpdateListDTOFactory(factory.Factory):
    class Meta:
        model = UpdateListDTO

    list_id = factory.Faker("uuid4")
    name = factory.Faker("word")
    description = factory.Faker("sentence")


class ListDTOFactory(factory.Factory):
    class Meta:
        model = ListDTO

    list_id = factory.Faker("uuid4")
    name = factory.Faker("word")
    description = factory.Faker("sentence")
    space_id = factory.Faker("uuid4")
    is_active = True
    order = factory.Faker("random_int", min=1, max=100)
    is_private = False
    created_by = factory.Faker("uuid4")
    folder_id = None


class CreateTaskDTOFactory(factory.Factory):
    class Meta:
        model = CreateTaskDTO

    title = factory.Faker('sentence', nb_words=3)
    description = factory.Faker('text')
    list_id = factory.Faker('uuid4')
    created_by = factory.Faker('uuid4')


class UpdateTaskDTOFactory(factory.Factory):
    class Meta:
        model = UpdateTaskDTO

    task_id = factory.Faker('uuid4')
    title = factory.Faker('sentence', nb_words=3)
    description = factory.Faker('text')


class TaskDTOFactory(factory.Factory):
    class Meta:
        model = TaskDTO

    task_id = factory.Faker('uuid4')
    title = factory.Faker('sentence', nb_words=3)
    description = factory.Faker('text')
    list_id = factory.Faker('uuid4')
    order = factory.sequence(lambda n: n + 1)
    created_by = factory.Faker('uuid4')
    is_deleted = False


class TaskAssigneeDTOFactory(factory.Factory):
    class Meta:
        model = TaskAssigneeDTO

    assign_id = factory.Faker('uuid4')
    user_id = factory.Faker('uuid4')
    task_id = factory.Faker('uuid4')
    assigned_by = factory.Faker('uuid4')
    is_active = True


class UserTasksDTOFactory(factory.Factory):
    class Meta:
        model = UserTasksDTO

    user_id = factory.Faker('uuid4')
    tasks = factory.List([
        factory.SubFactory(TaskDTOFactory) for _ in range(3)
    ])


class CreateFolderDTOFactory(factory.Factory):
    class Meta:
        model = CreateFolderDTO

    name = factory.Faker('word')
    description = factory.Faker('sentence')
    space_id = factory.Faker('uuid4')
    created_by = factory.Faker('uuid4')
    is_private = False


class UpdateFolderDTOFactory(factory.Factory):
    class Meta:
        model = UpdateFolderDTO

    folder_id = factory.Faker('uuid4')
    name = factory.Faker('word')
    description = factory.Faker('sentence')


class FolderDTOFactory(factory.Factory):
    class Meta:
        model = FolderDTO

    folder_id = factory.Faker('uuid4')
    name = factory.Faker('word')
    description = factory.Faker('sentence')
    space_id = factory.Faker('uuid4')
    order = factory.Sequence(lambda n: n + 1)
    is_active = True
    created_by = factory.Faker('uuid4')
    is_private = False


class CreateViewDTOFactory(factory.Factory):
    class Meta:
        model = CreateViewDTO

    name = factory.Faker('word')
    description = factory.Faker('sentence')
    view_type = factory.Iterator(['list', 'board', 'calendar', 'table'])
    created_by = factory.Faker('uuid4')


class UpdateViewDTOFactory(factory.Factory):
    class Meta:
        model = UpdateViewDTO

    view_id = factory.Faker('uuid4')
    name = factory.Faker('word')
    description = factory.Faker('sentence')


class ViewDTOFactory(factory.Factory):
    class Meta:
        model = ViewDTO

    view_id = factory.Faker('uuid4')
    name = factory.Faker('word')
    description = factory.Faker('sentence')
    view_type = factory.Iterator(['list', 'board', 'calendar', 'table'])
    created_by = factory.Faker('uuid4')


class ListViewDTOFactory(factory.Factory):
    class Meta:
        model = ListViewDTO

    id = factory.Sequence(lambda n: n + 1)
    list_id = factory.Faker('uuid4')
    view_id = factory.Faker('uuid4')
    applied_by = factory.Faker('uuid4')
    is_active = True


class RemoveListViewDTOFactory(factory.Factory):
    class Meta:
        model = RemoveListViewDTO

    id = factory.Sequence(lambda n: n + 1)
    list_id = factory.Faker('uuid4')
    view_id = factory.Faker('uuid4')
    removed_by = factory.Faker('uuid4')
    is_active = False


class CreateSpaceDTOFactory(factory.Factory):
    class Meta:
        model = CreateSpaceDTO

    name = factory.Faker('word')
    description = factory.Faker('sentence')
    workspace_id = factory.Faker('uuid4')
    is_private = False
    created_by = factory.Faker('uuid4')


class SpaceDTOFactory(factory.Factory):
    class Meta:
        model = SpaceDTO

    space_id = factory.Faker('uuid4')
    name = factory.Faker('word')
    description = factory.Faker('sentence')
    workspace_id = factory.Faker('uuid4')
    order = factory.Sequence(lambda n: n + 1)
    is_active = True
    is_private = False
    created_by = factory.Faker('uuid4')


class CreateWorkspaceFactory(factory.Factory):
    class Meta:
        model = CreateWorkspaceDTO

    name = factory.Faker('company')
    description = factory.Faker('sentence')
    user_id = factory.Faker('uuid4')
    account_id = factory.Faker('uuid4')


class WorkspaceDTOFactory(factory.Factory):
    class Meta:
        model = WorkspaceDTO

    workspace_id = factory.Faker('uuid4')
    name = factory.Faker('company')
    description = factory.Faker('sentence')
    user_id = factory.Faker('uuid4')
    account_id = factory.Faker('uuid4')
    is_active = True


# Aliases for backward compatibility
CreateFieldDTOFactory = CreateFieldFactory
FieldDTOFactory = FieldDTOFactory
CreateWorkspaceDTOFactory = CreateWorkspaceFactory
WorkspaceDTOFactory = WorkspaceDTOFactory


class AddMemberToWorkspaceDTOFactory(factory.Factory):
    class Meta:
        model = AddMemberToWorkspaceDTO

    workspace_id = factory.LazyFunction(lambda: str(uuid.uuid4()))
    user_id = factory.LazyFunction(lambda: str(uuid.uuid4()))
    added_by = factory.LazyFunction(lambda: str(uuid.uuid4()))
    role = Role.MEMBER


class WorkspaceMemberDTOFactory(factory.Factory):
    class Meta:
        model = WorkspaceMemberDTO

    id = factory.Sequence(lambda n: n + 1)
    workspace_id = factory.LazyFunction(lambda: str(uuid.uuid4()))
    user_id = factory.LazyFunction(lambda: str(uuid.uuid4()))
    role = Role.MEMBER
    is_active = factory.Faker('boolean')
    added_by = factory.LazyFunction(lambda: str(uuid.uuid4()))


class CreateAccountFactory(factory.Factory):
    class Meta:
        model = CreateAccountDTO

    name = factory.Faker("company")
    description = factory.Faker("sentence")
    owner_id = factory.Faker("uuid4")


class AccountDTOFactory(factory.Factory):
    class Meta:
        model = AccountDTO

    account_id = factory.Faker("uuid4")
    name = factory.Faker("company")
    description = factory.Faker("sentence")
    owner_id = factory.Faker("uuid4")
    is_active = True


class CreateAccountMemberFactory(factory.Factory):
    class Meta:
        model = CreateAccountMemberDTO

    account_id = factory.Faker("uuid4")
    user_id = factory.Faker("uuid4")
    role = Role.MEMBER
    added_by = factory.Faker("uuid4")


class AccountMemberDTOFactory(factory.Factory):
    class Meta:
        model = AccountMemberDTO

    id = factory.Sequence(lambda n: n + 1)
    account_id = factory.Faker("uuid4")
    user_id = factory.Faker("uuid4")
    role = Role.MEMBER
    is_active = True
    added_by = factory.Faker("uuid4")
