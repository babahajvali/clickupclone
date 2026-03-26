from django.urls import re_path

from task_management.consumers import TaskUpdatesConsumer
from task_management.websocket_auth import QueryStringJWTAuthMiddleware


websocket_urlpatterns = [
    re_path(
        r"ws/tasks/(?P<task_id>[0-9a-fA-F-]+)/$",
        QueryStringJWTAuthMiddleware(TaskUpdatesConsumer.as_asgi()),
    ),
    re_path(
        r"ws/lists/(?P<list_id>[0-9a-fA-F-]+)/$",
        QueryStringJWTAuthMiddleware(TaskUpdatesConsumer.as_asgi()),
    ),
]
