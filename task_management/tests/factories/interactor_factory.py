import factory

from task_management.interactors.dtos import CreateFieldDTO, FieldTypeEnum, \
    FieldDTO, CreateTemplateDTO, TemplateDTO, UpdateTemplateDTO, CreateListDTO, \
    UpdateListDTO, ListDTO


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
