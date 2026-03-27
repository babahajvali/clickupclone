"""
URL configuration for clickupclone project.

The `urlpatterns` lists routes URLs to list_views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function list_views
    1. Add an import:  from my_app import list_views
    2. Add a URL to urlpatterns:  path('', list_views.home, name='home')
Class-based list_views
    1. Add an import:  from other_app.list_views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

from clickupclone.schema import schema
from task_management.views import stripe_webhook

urlpatterns = [
    path("admin/", admin.site.urls),
    path('graphql/',
         csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
    path("webhook/stripe/", stripe_webhook, name="stripe_webhook"),
]
