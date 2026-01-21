import uuid
import factory
from factory.django import DjangoModelFactory
from faker import Faker

from task_management.models import (
    User, Account, AccountMember, Workspace, Space, Folder, List,
    Task, Template, View, ListView, TaskAssignee, Field, FieldValue,
    WorkspaceMember, SpacePermission, FolderPermission, ListPermission
)

faker = Faker()
faker.seed_instance(1)


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    user_id = factory.LazyFunction(uuid.uuid4)
    image_url = factory.Faker("image_url")
    full_name = factory.Faker("name")
    username = factory.Faker("user_name")
    password = "test123"
    email = factory.Faker("email")
    phone_number = factory.Faker("phone_number")
    gender = User.GenderType.MALE
    is_active = True


class AccountFactory(DjangoModelFactory):
    class Meta:
        model = Account

    account_id = factory.LazyFunction(uuid.uuid4)
    name = factory.Faker("company")
    description = factory.Faker("paragraph")
    owner = factory.SubFactory(UserFactory)
    is_active = True


class AccountMemberFactory(DjangoModelFactory):
    class Meta:
        model = AccountMember

    account = factory.SubFactory(AccountFactory)
    user = factory.SubFactory(UserFactory)
    role = "member"
    is_active = True
    added_by = factory.SubFactory(UserFactory)


class WorkspaceFactory(DjangoModelFactory):
    class Meta:
        model = Workspace

    workspace_id = factory.LazyFunction(uuid.uuid4)
    name = factory.Faker("word")
    description = factory.Faker("paragraph")
    account = factory.SubFactory(AccountFactory)
    created_by = factory.SubFactory(UserFactory)
    is_active = True


class WorkspaceMemberFactory(DjangoModelFactory):
    class Meta:
        model = WorkspaceMember

    workspace = factory.SubFactory(WorkspaceFactory)
    user = factory.SubFactory(UserFactory)
    role = "member"
    is_active = True
    added_by = factory.SubFactory(UserFactory)


class SpaceFactory(DjangoModelFactory):
    class Meta:
        model = Space

    space_id = factory.LazyFunction(uuid.uuid4)
    name = factory.Faker("word")
    description = factory.Faker("sentence")
    workspace = factory.SubFactory(WorkspaceFactory)
    order = factory.Sequence(lambda n: n + 1)
    is_active = True
    is_private = False
    created_by = factory.SubFactory(UserFactory)



class FolderFactory(DjangoModelFactory):
    class Meta:
        model = Folder

    folder_id = factory.LazyFunction(uuid.uuid4)
    name = factory.Faker("word")
    description = factory.Faker("sentence")
    space = factory.SubFactory(SpaceFactory)
    order = factory.Sequence(lambda n: n + 1)
    is_active = True
    is_private = False
    created_by = factory.SubFactory(UserFactory)



class ListFactory(DjangoModelFactory):
    class Meta:
        model = List

    list_id = factory.LazyFunction(uuid.uuid4)
    name = factory.Faker("word")
    description = factory.Faker("sentence")
    space = factory.SubFactory(SpaceFactory)
    folder = factory.SubFactory(FolderFactory)
    order = factory.Sequence(lambda n: n + 1)
    is_active = True
    is_private = False
    created_by = factory.SubFactory(UserFactory)


class TaskFactory(DjangoModelFactory):
    class Meta:
        model = Task

    task_id = factory.LazyFunction(uuid.uuid4)
    title = factory.Faker("sentence")
    description = factory.Faker("paragraph")
    list = factory.SubFactory(ListFactory)
    order = factory.Sequence(lambda n: n + 1)
    is_deleted = False
    created_by = factory.SubFactory(UserFactory)


class TaskAssigneeFactory(DjangoModelFactory):
    class Meta:
        model = TaskAssignee

    assign_id = factory.LazyFunction(uuid.uuid4)
    task = factory.SubFactory(TaskFactory)
    user = factory.SubFactory(UserFactory)
    is_active = True
    assigned_by = factory.SubFactory(UserFactory)


class TemplateFactory(DjangoModelFactory):
    class Meta:
        model = Template

    template_id = factory.LazyFunction(uuid.uuid4)
    name = factory.Faker("word")
    description = factory.Faker("sentence")
    list = factory.SubFactory(ListFactory)


class ViewFactory(DjangoModelFactory):
    class Meta:
        model = View

    view_id = factory.LazyFunction(uuid.uuid4)
    name = factory.Faker("word")
    description = factory.Faker("sentence")
    view_type = View.ViewType.LIST
    created_by = factory.SubFactory(UserFactory)


class ListViewFactory(DjangoModelFactory):
    class Meta:
        model = ListView

    list = factory.SubFactory(ListFactory)
    view = factory.SubFactory(ViewFactory)
    is_active = True
    applied_by = factory.SubFactory(UserFactory)


class FieldFactory(DjangoModelFactory):
    class Meta:
        model = Field

    field_id = factory.LazyFunction(uuid.uuid4)
    field_name = factory.Faker("word")
    description = factory.Faker("sentence")
    field_type = Field.FieldType.TEXT
    template = factory.SubFactory(TemplateFactory)
    order = factory.Sequence(lambda n: n + 1)
    config = {}
    is_required = False
    is_active = True
    created_by = factory.SubFactory(UserFactory)


class FieldValueFactory(DjangoModelFactory):
    class Meta:
        model = FieldValue

    field = factory.SubFactory(FieldFactory)
    task = factory.SubFactory(TaskFactory)
    value = {"text": "sample"}
    created_by = factory.SubFactory(UserFactory)


class SpacePermissionFactory(DjangoModelFactory):
    class Meta:
        model = SpacePermission

    space = factory.SubFactory(SpaceFactory)
    user = factory.SubFactory(UserFactory)
    permission_type = "view"
    is_active = True
    added_by = factory.SubFactory(UserFactory)


class FolderPermissionFactory(DjangoModelFactory):
    class Meta:
        model = FolderPermission

    folder = factory.SubFactory(FolderFactory)
    user = factory.SubFactory(UserFactory)
    permission_type = "view"
    is_active = True
    added_by = factory.SubFactory(UserFactory)


class ListPermissionFactory(DjangoModelFactory):
    class Meta:
        model = ListPermission

    list = factory.SubFactory(ListFactory)
    user = factory.SubFactory(UserFactory)
    permission_type = "view"
    is_active = True
    added_by = factory.SubFactory(UserFactory)
