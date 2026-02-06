# task_management/management/commands/create_test_plans.py

from django.core.management.base import BaseCommand
from task_management.models import Plan


class Command(BaseCommand):
    help = 'Create test Stripe plans'

    def handle(self, *args, **kwargs):
        plans = [
            {
                'plan_name': 'pro',
                'stripe_price_id': 'price_1234567890',
                # Replace with your Stripe Price ID
                'price': 9.99,
                'currency': 'USD',
                'billing_period': 'month',
                'features': {
                    'max_lists': 50,
                    'max_tasks_per_list': 1000,
                    'custom_fields': True,
                    'priority_support': True
                }
            },
            {
                'plan_name': 'enterprise',
                'stripe_price_id': 'price_0987654321',
                # Replace with your Stripe Price ID
                'price': 29.99,
                'currency': 'USD',
                'billing_period': 'month',
                'features': {
                    'max_lists': -1,  # Unlimited
                    'max_tasks_per_list': -1,
                    'custom_fields': True,
                    'priority_support': True,
                    'api_access': True,
                    'dedicated_account_manager': True
                }
            }
        ]

        for plan_data in plans:
            plan, created = Plan.objects.get_or_create(
                stripe_price_id=plan_data['stripe_price_id'],
                defaults=plan_data
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Created plan: {plan.plan_name}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Plan already exists: {plan.plan_name}")
                )