from django.shortcuts import render

# Create your views here.
# task_management/views/stripe_webhook_view.py

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from task_management.interactors.webhook_handler_interactor import \
    WebhookHandlerInteractor
from task_management.storages.subscription_storage import SubscriptionStorage
from task_management.storages.payment_storage import PaymentStorage
from task_management.storages.plan_storage import PlanStorage
from task_management.exceptions.custom_exceptions import StripeWebhookException
import logging

logger = logging.getLogger(__name__)


@csrf_exempt
@require_POST
def stripe_webhook(request):
    """Handle incoming webhooks from Stripe"""

    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    if not sig_header:
        return JsonResponse({'error': 'Missing signature'}, status=400)

    interactor = WebhookHandlerInteractor(
        subscription_storage=SubscriptionStorage(),
        payment_storage=PaymentStorage(),
        plan_storage=PlanStorage()
    )

    try:
        result = interactor.handle_webhook_event(
            payload=payload.decode('utf-8'),
            sig_header=sig_header
        )

        logger.info(f"Webhook processed: {result}")
        return JsonResponse(result, status=200)

    except StripeWebhookException as e:
        logger.error(f"Webhook error: {e.message}")
        return JsonResponse({'error': e.message}, status=400)

    except Exception as e:
        logger.error(f"Unexpected webhook error: {str(e)}")
        return JsonResponse({'error': 'Internal server error'}, status=500)