# task_management/urls.py

from django.urls import path
from task_management.views import stripe_webhook

urlpatterns = [
    # ... your existing URLs
    path('webhook/stripe/', stripe_webhook, name='stripe_webhook'),
]