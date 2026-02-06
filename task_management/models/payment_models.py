# task_management/models/subscription.py

from django.db import models
import uuid


class Plan(models.Model):
    PLAN_TYPES = (
        ('free', 'Free'),
        ('pro', 'Pro'),
        ('enterprise', 'Enterprise'),
    )

    BILLING_PERIODS = (
        ('month', 'Monthly'),
        ('year', 'Yearly'),
    )

    plan_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                               editable=False)
    plan_name = models.CharField(max_length=50, choices=PLAN_TYPES)
    stripe_price_id = models.CharField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    billing_period = models.CharField(max_length=10, choices=BILLING_PERIODS)
    features = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'plans'

    def __str__(self):
        return f"{self.plan_name} - {self.billing_period}"


class Customer(models.Model):
    customer_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                   editable=False)
    user = models.OneToOneField("User", on_delete=models.CASCADE,
                                related_name='stripe_customer')
    stripe_customer_id = models.CharField(max_length=255, unique=True)
    default_payment_method = models.CharField(max_length=255, blank=True,
                                              null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'customers'

    def __str__(self):
        return f"Customer: {self.user.username}"


class Subscription(models.Model):
    SUBSCRIPTION_STATUS = (
        ('active', 'Active'),
        ('canceled', 'Canceled'),
        ('past_due', 'Past Due'),
        ('unpaid', 'Unpaid'),
        ('trialing', 'Trialing'),
        ('incomplete', 'Incomplete'),
    )

    subscription_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                       editable=False)
    user = models.ForeignKey("User", on_delete=models.CASCADE,
                             related_name='subscriptions')
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True,
                             related_name='subscriptions')
    stripe_subscription_id = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=20, choices=SUBSCRIPTION_STATUS)
    current_period_start = models.DateTimeField()
    current_period_end = models.DateTimeField()
    cancel_at_period_end = models.BooleanField(default=False)
    canceled_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'subscriptions'

    def __str__(self):
        return f"{self.user.username} - {self.plan.plan_name if self.plan else 'No Plan'}"


class Payment(models.Model):
    PAYMENT_STATUS = (
        ('succeeded', 'Succeeded'),
        ('failed', 'Failed'),
        ('pending', 'Pending'),
        ('canceled', 'Canceled'),
    )

    payment_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                  editable=False)
    user = models.ForeignKey("User", on_delete=models.CASCADE,
                             related_name='payments')
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL,
                                     null=True, blank=True,
                                     related_name='payments')
    stripe_payment_intent_id = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS)
    payment_method = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'payments'
        ordering = ['-created_at']

    def __str__(self):
        return f"Payment {self.payment_id} - {self.status}"