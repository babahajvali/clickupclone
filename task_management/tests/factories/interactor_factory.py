import factory

from task_management.exceptions.enums import FieldTypeEnum
from task_management.interactors.dtos import CreateFieldDTO,  \
    FieldDTO, CreateTemplateDTO, TemplateDTO, UpdateTemplateDTO, CreateListDTO, \
    UpdateListDTO, ListDTO, CreateTaskDTO, UpdateTaskDTO, TaskDTO, TaskAssigneeDTO, \
    RemoveTaskAssigneeDTO, UserTasksDTO, CreateFolderDTO, UpdateFolderDTO, FolderDTO


class CreateFieldFactory(factory.Factory):
    class Meta:
        model = CreateFieldDTO

    template_id = factory.Faker("uuid4")
    field_name = factory.Faker("name")
    description = factory.Faker("text")
    field_type = factory.Iterator([x.value for x in FieldTypeEnum])
    order = factory.sequence(lambda n: n + 1)
    is_required = factory.Faker("boolean")
    created_by = factory.Faker("uuid4")


class FieldDTOFactory(factory.Factory):
    class Meta:
        model = FieldDTO

    field_id = factory.Faker("uuid4")
    template_id = factory.Faker("uuid4")
    field_name = factory.Faker("name")
    description = factory.Faker("text")
    field_type = factory.Iterator([x.value for x in FieldTypeEnum])
    order = factory.sequence(lambda n: n + 1)
    is_required = factory.Faker("boolean")
    created_by = factory.Faker("uuid4")


class CreateTemplateDTOFactory(factory.Factory):
    class Meta:
        model = CreateTemplateDTO

    name = factory.Faker("word")
    description = factory.Faker("sentence")
    list_id = factory.Faker("uuid4")
    is_default = False
    created_by = factory.Faker("uuid4")

class UpdateTemplateDTOFactory(factory.Factory):
    class Meta:
        model = UpdateTemplateDTO

    template_id = factory.Faker("uuid4")
    name = factory.Faker("word")
    list_id = factory.Faker("uuid4")
    description = factory.Faker("sentence")
    is_default = False
    created_by = factory.Faker("uuid4")


class TemplateDTOFactory(factory.Factory):
    class Meta:
        model = TemplateDTO

    template_id = factory.Faker("uuid4")
    name = factory.Faker("word")
    list_id = factory.Faker("uuid4")
    description = factory.Faker("sentence")
    is_default = False
    created_by = factory.Faker("uuid4")

class CreateListDTOFactory(factory.Factory):
    class Meta:
        model = CreateListDTO

    name = factory.Faker("word")
    description = factory.Faker("sentence")
    space_id = factory.Faker("uuid4")
    order = factory.Faker("random_int", min=1, max=100)
    is_active = True
    is_private = False
    created_by = factory.Faker("uuid4")
    folder_id = None

class UpdateListDTOFactory(factory.Factory):
    class Meta:
        model = UpdateListDTO

    list_id = factory.Faker("uuid4")
    name = factory.Faker("word")
    description = factory.Faker("sentence")
    space_id = factory.Faker("uuid4")
    is_active = True
    order = factory.Faker("random_int", min=1, max=100)
    is_private = False
    created_by = factory.Faker("uuid4")
    folder_id = None


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
    is_active = True


class UpdateTaskDTOFactory(factory.Factory):
    class Meta:
        model = UpdateTaskDTO

    task_id = factory.Faker('uuid4')
    title = factory.Faker('sentence', nb_words=3)
    description = factory.Faker('text')
    list_id = factory.Faker('uuid4')
    created_by = factory.Faker('uuid4')
    is_active = True


class TaskDTOFactory(factory.Factory):
    class Meta:
        model = TaskDTO

    task_id = factory.Faker('uuid4')
    title = factory.Faker('sentence', nb_words=3)
    description = factory.Faker('text')
    list_id = factory.Faker('uuid4')
    created_by = factory.Faker('uuid4')
    is_active = True


class TaskAssigneeDTOFactory(factory.Factory):
    class Meta:
        model = TaskAssigneeDTO

    assignee_id = factory.Faker('uuid4')
    assignee_name = factory.Faker('name')
    task_id = factory.Faker('uuid4')
    assigned_by = factory.Faker('uuid4')
    is_active = True


class RemoveTaskAssigneeDTOFactory(factory.Factory):
    class Meta:
        model = RemoveTaskAssigneeDTO

    task_id = factory.Faker('uuid4')
    assignee_id = factory.Faker('uuid4')
    removed_by = factory.Faker('uuid4')
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
    order = factory.Sequence(lambda n: n + 1)
    is_active = True
    created_by = factory.Faker('uuid4')
    is_private = False


class UpdateFolderDTOFactory(factory.Factory):
    class Meta:
        model = UpdateFolderDTO

    folder_id = factory.Faker('uuid4')
    name = factory.Faker('word')
    description = factory.Faker('sentence')
    space_id = factory.Faker('uuid4')
    order = factory.Sequence(lambda n: n + 1)
    is_active = True
    created_by = factory.Faker('uuid4')
    is_private = False


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
