from django.core.exceptions import ObjectDoesNotExist

from task_management.exceptions.enums import ViewTypes
from task_management.interactors.dtos import ViewDTO, CreateViewDTO, \
    UpdateViewDTO, ListViewDTO
from task_management.interactors.storage_interfaces.view_storage_interface import \
    ViewStorageInterface
from task_management.models import View, User, List, ListView


class ViewStorage(ViewStorageInterface):
    @staticmethod
    def _view_dto(data: View) -> ViewDTO:
        view_type = ViewTypes(data.view_type)
        return ViewDTO(
            view_id=data.view_id,
            name=data.name,
            description=data.description,
            view_type=view_type,
            created_by=data.created_by.user_id,
        )

    def get_all_views(self) -> list[ViewDTO]:
        views = View.objects.all()
        return [self._view_dto(data=view_data) for view_data in views]

    def get_view(self, view_id: str) -> ViewDTO:
        view_data = View.objects.get(view_id=view_id)

        return self._view_dto(data=view_data)

    def create_view(self, create_view_data: CreateViewDTO) -> ViewDTO:
        user = User.objects.get(user_id=create_view_data.created_by)
        view_data = View.objects.create(
            name=create_view_data.name,
            view_type=create_view_data.view_type.value,
            description=create_view_data.description, created_by=user)

        return self._view_dto(data=view_data)

    def update_view(self, view_id: str, field_properties: dict) -> ViewDTO:

        View.objects.filter(view_id=view_id).update(**field_properties)
        view_data = View.objects.get(view_id=view_id)

        return self._view_dto(data=view_data)

    def check_view_exists(self, view_id: str) -> bool:

        return View.objects.filter(view_id=view_id).exists()

    def apply_view_for_list(self, list_id: str, view_id: str,
                            user_id: str) -> ListViewDTO:
        list_obj = List.objects.get(list_id=list_id)
        view = View.objects.get(view_id=view_id)
        user = User.objects.get(user_id=user_id)

        list_view_data = ListView.objects.create(list=list_obj, view=view,
                                                 applied_by=user)

        return ListViewDTO(
            id=list_view_data.pk,
            list_id=list_view_data.list.list_id,
            view_id=list_view_data.view.view_id,
            applied_by=list_view_data.applied_by.user_id,
            is_active=list_view_data.is_active,
        )

    def remove_list_view(self, view_id: str, list_id: str):
        # set the is_active is false
        list_view_obj = ListView.objects.get(list_id=list_id, view_id=view_id)
        list_view_obj.is_active = False
        list_view_obj.save()

        return ListViewDTO(
            id=list_view_obj.pk,
            list_id=list_id,
            view_id=view_id,
            applied_by=list_view_obj.applied_by.user_id,
            is_active=list_view_obj.is_active,
        )

    def get_list_views(self, list_id: str) -> list[ListViewDTO]:
        # get the active list_view only

        list_views = ListView.objects.filter(list_id=list_id, is_active=True)

        return [ListViewDTO(
            id=list_view_data.pk,
            list_id=list_view_data.list.list_id,
            view_id=list_view_data.view.view_id,
            applied_by=list_view_data.applied_by.user_id,
            is_active=list_view_data.is_active,
        ) for list_view_data in list_views]

    def is_list_view_exist(self, list_id: str, view_id: str) -> bool:
        return ListView.objects.filter(list_id=list_id,
                                       view_id=view_id).exists()

    def get_list_view(self, list_id: str, view_id: str) -> ListViewDTO | None:
        try:
            list_view_data = ListView.objects.get(
                list_id=list_id, view_id=view_id, is_active=True)

            return ListViewDTO(
                id=list_view_data.pk,
                list_id=list_view_data.list.list_id,
                view_id=list_view_data.view.view_id,
                applied_by=list_view_data.applied_by.user_id,
                is_active=list_view_data.is_active,
            )
        except ObjectDoesNotExist:
            return None

    def get_list_view_id(self, view_type: str) -> str:
        view_data = View.objects.get(view_type=view_type)

        return view_data.view_id
