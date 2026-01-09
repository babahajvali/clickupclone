from task_management.interactors.dtos import TemplateDTO, CreateTemplateDTO, \
    UpdateTemplateDTO
from task_management.interactors.storage_interface.template_storage_interface import \
    TemplateStorageInterface
from task_management.models import Template, List


class TemplateStorage(TemplateStorageInterface):

    @staticmethod
    def _template_dto(data: Template) -> TemplateDTO:
        return TemplateDTO(
            template_id=data.template_id,
            name=data.name,
            description=data.description,
            list_id=data.list.list_id,
            created_by=data.list.created_by.user_id,
        )

    def get_template_by_id(self, template_id: str) -> TemplateDTO:
        template_data = Template.objects.get(template_id=template_id)

        return self._template_dto(data=template_data)

    def create_template(self, template_data: CreateTemplateDTO) -> TemplateDTO:
        list_obj = List.objects.get(list_id=template_data.list_id)
        template_data = Template.objects.create(name=template_data.name,
                                                description=template_data.description,
                                                list=list_obj)

        return self._template_dto(data=template_data)

    def is_template_name_exist(self, template_name: str) -> bool:
        return Template.objects.filter(name=template_name).exists()

    def check_template_name_exist_except_this_template(self,
                                                       template_name: str,
                                                       template_id: str) -> bool:
        return Template.objects.filter(name=template_name).exclude(
            template_id=template_id).exists()

    def update_template(self,
                        update_template_data: UpdateTemplateDTO) -> TemplateDTO:
        template_data = Template.objects.get(template_id=update_template_data.template_id)
        if update_template_data.name:
            template_data.name = update_template_data.name

        if update_template_data.description:
            template_data.description = update_template_data.description

        template_data.save()

        return self._template_dto(data=template_data)
