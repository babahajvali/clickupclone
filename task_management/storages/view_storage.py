from task_management.interactors.dtos import ListViewDTO, CreateListViewDTO
from task_management.interactors.storage_interfaces import ViewStorageInterface

from task_management.models import ListView


class ViewStorage(ViewStorageInterface):

    @staticmethod
    def _convert_list_view_to_dto(list_view_obj: ListView) -> ListViewDTO:
        return ListViewDTO(
            id=list_view_obj.pk,
            view_name=list_view_obj.view_type.capitalize(),
            list_id=list_view_obj.list_id,
            view_type=list_view_obj.view_type,
            created_by=list_view_obj.created_by_id,
            is_active=list_view_obj.is_active,
        )

    def create_list_view(
            self, create_list_view_dto: CreateListViewDTO) -> ListViewDTO:
        list_view_obj = ListView.objects.create(
            list_id=create_list_view_dto.list_id,
            view_type=create_list_view_dto.view_type.value,
            created_by_id=create_list_view_dto.created_by)

        return self._convert_list_view_to_dto(list_view_obj=list_view_obj)

    def remove_list_view(self, list_view_id: int) -> ListViewDTO:
        ListView.objects.filter(pk=list_view_id).update(is_active=False)

        return self.get_list_view_by_id(list_view_id=list_view_id)

    def get_list_views(self, list_id: str) -> list[ListViewDTO]:
        list_view_objs = ListView.objects.filter(
            list_id=list_id, is_active=True)

        return [self._convert_list_view_to_dto(list_view_obj=list_view_obj)
                for list_view_obj in list_view_objs]

    def is_list_view_exist(self, list_view_id: int) -> bool:
        return ListView.objects.filter(pk=list_view_id).exists()

    def get_list_view(self, list_id: str,
                      view_type: str) -> ListViewDTO | None:
        list_view_dto = ListView.objects.filter(
            list_id=list_id, view_type=view_type, is_active=True).first()

        if list_view_dto is None:
            return None

        return self._convert_list_view_to_dto(list_view_obj=list_view_dto)

    def get_list_view_by_id(self, list_view_id: int) -> ListViewDTO:
        list_view_dto = ListView.objects.filter(pk=list_view_id).first()

        return self._convert_list_view_to_dto(list_view_obj=list_view_dto)
