from django.core.exceptions import ObjectDoesNotExist

from task_management.interactors.dtos import ListViewDTO, RemoveListViewDTO
from task_management.interactors.storage_interface.list_views_storage_interface import \
    ListViewsStorageInterface
from task_management.models import List, View, User, ListView


class ListViewStorage(ListViewsStorageInterface):

    def apply_view_for_list(self, list_id: str, view_id: str,
                            user_id: str) -> ListViewDTO:
        list_obj = List.objects.get(list_id=list_id)
        view = View.objects.get(view_id=view_id)
        user = User.objects.get(user_id=user_id)

        list_view_data = ListView.objects.create(list=list_obj, view=view, applied_by=user)

        return ListViewDTO(
            id=list_view_data.pk,
            list_id=list_view_data.list.list_id,
            view_id=list_view_data.view.view_id,
            applied_by=list_view_data.applied_by.user_id,
            is_active=list_view_data.is_active,
        )

    def remove_view_for_list(self, view_id: str, list_id: str):
        # set the is_active is false
        list_view_obj = ListView.objects.get(list_id=list_id,view_id=view_id)
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

        list_views = ListView.objects.filter(list_id=list_id,is_active=True)

        return [ListViewDTO(
            id=list_view_data.pk,
            list_id=list_view_data.list.list_id,
            view_id=list_view_data.view.view_id,
            applied_by=list_view_data.applied_by.user_id,
            is_active=list_view_data.is_active,
        )for list_view_data in list_views]

    def is_list_view_exist(self, list_id: str, view_id: str) -> bool:
        return ListView.objects.filter(list_id=list_id,view_id=view_id).exists()

    def get_list_view(self,list_id: str, view_id: str) -> ListViewDTO | None:
        try:
            list_view_data = ListView.objects.get(list_id=list_id,view_id=view_id)

            return ListViewDTO(
                id=list_view_data.pk,
                list_id=list_view_data.list.list_id,
                view_id=list_view_data.view.view_id,
                applied_by=list_view_data.applied_by.user_id,
                is_active=list_view_data.is_active,
            )
        except ObjectDoesNotExist:
            return None
