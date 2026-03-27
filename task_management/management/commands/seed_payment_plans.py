from django.core.management.base import BaseCommand

from task_management.models import Plan


EXAMPLE_PLANS = [
    {
        "plan_name": "free",
        "stripe_price_id": "price_free_monthly_demo",
        "price": "0.00",
        "currency": "USD",
        "billing_period": "month",
        "features": {
            "members": 3,
            "storage_gb": 1,
            "custom_fields": False,
            "automation_limit": 0,
        },
        "is_active": True,
    },
    {
        "plan_name": "pro",
        "stripe_price_id": "price_pro_monthly_demo",
        "price": "9.99",
        "currency": "USD",
        "billing_period": "month",
        "features": {
            "members": 25,
            "storage_gb": 100,
            "custom_fields": True,
            "automation_limit": 1000,
        },
        "is_active": True,
    },
    {
        "plan_name": "pro",
        "stripe_price_id": "price_pro_yearly_demo",
        "price": "99.99",
        "currency": "USD",
        "billing_period": "year",
        "features": {
            "members": 25,
            "storage_gb": 100,
            "custom_fields": True,
            "automation_limit": 12000,
        },
        "is_active": True,
    },
    {
        "plan_name": "enterprise",
        "stripe_price_id": "price_enterprise_yearly_demo",
        "price": "249.99",
        "currency": "USD",
        "billing_period": "year",
        "features": {
            "members": 250,
            "storage_gb": 1000,
            "custom_fields": True,
            "automation_limit": 100000,
            "priority_support": True,
            "sso": True,
        },
        "is_active": True,
    },
]


class Command(BaseCommand):
    help = "Seed example payment plans into the database"

    def handle(self, *args, **options):
        created_count = 0
        updated_count = 0

        for plan_data in EXAMPLE_PLANS:
            _, created = Plan.objects.update_or_create(
                stripe_price_id=plan_data["stripe_price_id"],
                defaults=plan_data,
            )
            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded payment plans: created={created_count}, updated={updated_count}"
            )
        )
