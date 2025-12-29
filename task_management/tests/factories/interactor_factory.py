import factory

from task_management.interactors.dtos import CreateFieldDTO, FieldTypeEnum, \
    FieldDTO


class CreateFieldFactory(factory.Factory):
    class Meta:
        model = CreateFieldDTO

    template_id = factory.Faker("uuid4")
    field_name = factory.Faker("name")
    description = factory.Faker("text")
    field_type = factory.iterator([x.value for x in FieldTypeEnum])
    order = factory.sequence(lambda n: n + 1)
    is_required = factory.boolean(default=False)
    created_by = factory.Faker("uuid4")


class FieldDTOFactory(factory.Factory):
    class Meta:
        model = FieldDTO

    field_id = factory.Faker("uuid4")
    template_id = factory.Faker("uuid4")
    field_name = factory.Faker("name")
    description = factory.Faker("text")
    field_type = factory.iterator([x.value for x in FieldTypeEnum])
    order = factory.sequence(lambda n: n + 1)
    is_required = factory.boolean(default=False)
    created_by = factory.Faker("uuid4")
