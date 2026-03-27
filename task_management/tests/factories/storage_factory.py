import uuid
from datetime import timedelta

import factory
from factory.django import DjangoModelFactory
from faker import Faker
from django.utils import timezone

from task_management.exceptions.enums import Gender, ViewType, FieldType
from task_management.exceptions.enums import ListEntityType
from task_management.models import (
    User, Account, Workspace, Space, Folder, List,
    Task, Template, ListView, TaskAssignee, Field, TaskFieldValue,
    WorkspaceMember, SpacePermission, FolderPermission, ListPermission,
    Plan, Customer, Subscription, Payment
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
    gender = Gender.MALE.value
    is_active = True


class AccountFactory(DjangoModelFactory):
    class Meta:
        model = Account

    account_id = factory.LazyFunction(uuid.uuid4)
    name = factory.Faker("company")
    description = factory.Faker("paragraph")
    owner = factory.SubFactory(UserFactory)
    is_active = True


class WorkspaceFactory(DjangoModelFactory):
    class Meta:
        model = Workspace

    workspace_id = factory.LazyFunction(uuid.uuid4)
    name = factory.Faker("word")
    description = factory.Faker("paragraph")
    account = factory.SubFactory(AccountFactory)
    created_by = factory.SubFactory(UserFactory)
    is_deleted = False


class WorkspaceMemberFactory(DjangoModelFactory):
    class Meta:
        model = WorkspaceMember

    id = factory.Sequence(lambda n: n)
    workspace = factory.SubFactory(WorkspaceFactory)
    user = factory.SubFactory(UserFactory)
    role = "MEMBER"
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
    is_deleted = False
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
    is_deleted = True
    is_private = False
    created_by = factory.SubFactory(UserFactory)


class ListFactory(DjangoModelFactory):
    class Meta:
        model = List

    list_id = factory.LazyFunction(uuid.uuid4)
    name = factory.Faker("word")
    description = factory.Faker("sentence")
    entity_type = ListEntityType.SPACE.value
    entity_id = factory.LazyFunction(lambda: str(uuid.uuid4()))
    order = factory.Sequence(lambda n: n + 1)
    is_deleted = False
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


class ListViewFactory(DjangoModelFactory):
    class Meta:
        model = ListView

    list = factory.SubFactory(ListFactory)
    view_type = ViewType.TABLE.value
    is_active = True
    created_by = factory.SubFactory(UserFactory)


class FieldFactory(DjangoModelFactory):
    class Meta:
        model = Field

    field_id = factory.LazyFunction(uuid.uuid4)
    field_name = factory.Faker("word")
    description = factory.Faker("sentence")
    field_type = FieldType.TEXT.value
    template = factory.SubFactory(TemplateFactory)
    order = factory.Sequence(lambda n: n + 1)
    config = {}
    is_required = False
    is_deleted = False
    created_by = factory.SubFactory(UserFactory)


class FieldValueFactory(DjangoModelFactory):
    class Meta:
        model = TaskFieldValue

    field = factory.SubFactory(FieldFactory)
    task = factory.SubFactory(TaskFactory)
    value = {"text": "sample"}
    created_by = factory.SubFactory(UserFactory)


class SpacePermissionFactory(DjangoModelFactory):
    class Meta:
        model = SpacePermission

    space = factory.SubFactory(SpaceFactory)
    user = factory.SubFactory(UserFactory)
    permission_type = "VIEW"
    is_active = True
    added_by = factory.SubFactory(UserFactory)


class FolderPermissionFactory(DjangoModelFactory):
    class Meta:
        model = FolderPermission

    folder = factory.SubFactory(FolderFactory)
    user = factory.SubFactory(UserFactory)
    permission_type = "list_views"
    is_active = True
    added_by = factory.SubFactory(UserFactory)


class ListPermissionFactory(DjangoModelFactory):
    class Meta:
        model = ListPermission

    list = factory.SubFactory(ListFactory)
    user = factory.SubFactory(UserFactory)
    permission_type = "list_views"
    is_active = True
    added_by = factory.SubFactory(UserFactory)


class PlanFactory(DjangoModelFactory):
    class Meta:
        model = Plan

    plan_id = factory.LazyFunction(uuid.uuid4)
    plan_name = "pro"
    stripe_price_id = factory.Sequence(lambda n: f"price_{n}")
    price = "9.99"
    currency = "USD"
    billing_period = "month"
    features = {}
    is_active = True


class CustomerFactory(DjangoModelFactory):
    class Meta:
        model = Customer

    customer_id = factory.LazyFunction(uuid.uuid4)
    user = factory.SubFactory(UserFactory)
    stripe_customer_id = factory.Sequence(lambda n: f"cus_{n}")
    default_payment_method = None


class SubscriptionFactory(DjangoModelFactory):
    class Meta:
        model = Subscription

    subscription_id = factory.LazyFunction(uuid.uuid4)
    user = factory.SubFactory(UserFactory)
    plan = factory.SubFactory(PlanFactory)
    stripe_subscription_id = factory.Sequence(lambda n: f"sub_{n}")
    status = "active"
    current_period_start = factory.LazyFunction(timezone.now)
    current_period_end = factory.LazyAttribute(
        lambda obj: obj.current_period_start + timedelta(days=30)
    )
    cancel_at_period_end = False
    canceled_at = None


class PaymentFactory(DjangoModelFactory):
    class Meta:
        model = Payment

    payment_id = factory.LazyFunction(uuid.uuid4)
    user = factory.SubFactory(UserFactory)
    subscription = factory.SubFactory(SubscriptionFactory)
    stripe_payment_intent_id = factory.Sequence(lambda n: f"pi_{n}")
    amount = "9.99"
    currency = "USD"
    status = "succeeded"
    payment_method = "card"
