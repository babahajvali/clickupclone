from django.core.exceptions import ObjectDoesNotExist

from task_management.interactors.dtos import TemplateDTO, CreateTemplateDTO
from task_management.interactors.storage_interfaces.template_storage_interface import \
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

    def validate_template_exists(self, template_id: str) -> bool:
        return Template.objects.filter(template_id=template_id).exists()

    def check_template_name_exist_except_this_template(self,
                                                       template_name: str,
                                                       template_id: str) -> bool:
        return Template.objects.filter(name=template_name).exclude(
            template_id=template_id).exists()

    def update_template(self, template_id: str,
                        update_fields: dict) -> TemplateDTO:
        Template.objects.filter(template_id=template_id).update(
            **update_fields)
        template_data = Template.objects.get(template_id=template_id)

        return self._template_dto(data=template_data)

    def get_template_list_id(self, template_id: str) -> str:
        return Template.objects.filter(list_id=template_id).values_list(
            'list_id', flat=True)[0]

    def get_workspace_id_from_template_id(self,
                                          template_id: str) -> str | None:
        try:
            template_data = Template.objects.select_related(
                "list__space__workspace").get(
                template_id=template_id)

            return template_data.list.space.workspace.workspace_id
        except ObjectDoesNotExist:
            return None
