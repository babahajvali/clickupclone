import logging

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from task_management.exceptions.custom_exceptions import StripeWebhookException
from task_management.interactors.payments.webhook_handler_interactor import (
    WebhookHandlerInteractor,
)
from task_management.storages.payment_storage import PaymentStorage
from task_management.storages.plan_storage import PlanStorage
from task_management.storages.subscription_storage import SubscriptionStorage

logger = logging.getLogger(__name__)


@csrf_exempt
@require_POST
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    if not sig_header:
        return JsonResponse({"error": "Missing signature"}, status=400)

    interactor = WebhookHandlerInteractor(
        subscription_storage=SubscriptionStorage(),
        payment_storage=PaymentStorage(),
        plan_storage=PlanStorage(),
    )

    try:
        result = interactor.handle_webhook_event(
            payload=payload,
            sig_header=sig_header,
        )
    except StripeWebhookException as exc:
        logger.error("Webhook error: %s", exc.message)
        return JsonResponse({"error": exc.message}, status=400)
    except Exception:
        logger.exception("Unexpected webhook error")
        return JsonResponse({"error": "Internal server error"}, status=500)

    return JsonResponse(result, status=200)
