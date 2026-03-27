from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("task_management", "0002_listview_view_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="Plan",
            fields=[
                (
                    "plan_id",
                    models.UUIDField(
                        primary_key=True,
                        default=uuid.uuid4,
                        editable=False,
                        serialize=False,
                    ),
                ),
                ("plan_name", models.CharField(choices=[("free", "Free"), ("pro", "Pro"), ("enterprise", "Enterprise")], max_length=50)),
                ("stripe_price_id", models.CharField(max_length=255, unique=True)),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("currency", models.CharField(default="USD", max_length=3)),
                ("billing_period", models.CharField(choices=[("month", "Monthly"), ("year", "Yearly")], max_length=10)),
                ("features", models.JSONField(blank=True, default=dict)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"db_table": "plans"},
        ),
        migrations.CreateModel(
            name="Customer",
            fields=[
                (
                    "customer_id",
                    models.UUIDField(
                        primary_key=True,
                        default=uuid.uuid4,
                        editable=False,
                        serialize=False,
                    ),
                ),
                ("stripe_customer_id", models.CharField(max_length=255, unique=True)),
                ("default_payment_method", models.CharField(blank=True, max_length=255, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="stripe_customer",
                        to="task_management.user",
                    ),
                ),
            ],
            options={"db_table": "customers"},
        ),
        migrations.CreateModel(
            name="Subscription",
            fields=[
                (
                    "subscription_id",
                    models.UUIDField(
                        primary_key=True,
                        default=uuid.uuid4,
                        editable=False,
                        serialize=False,
                    ),
                ),
                ("stripe_subscription_id", models.CharField(max_length=255, unique=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("active", "Active"),
                            ("canceled", "Canceled"),
                            ("past_due", "Past Due"),
                            ("unpaid", "Unpaid"),
                            ("trialing", "Trialing"),
                            ("incomplete", "Incomplete"),
                            ("incomplete_expired", "Incomplete Expired"),
                        ],
                        max_length=20,
                    ),
                ),
                ("current_period_start", models.DateTimeField()),
                ("current_period_end", models.DateTimeField()),
                ("cancel_at_period_end", models.BooleanField(default=False)),
                ("canceled_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "plan",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="subscriptions",
                        to="task_management.plan",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="subscriptions",
                        to="task_management.user",
                    ),
                ),
            ],
            options={"db_table": "subscriptions"},
        ),
        migrations.CreateModel(
            name="Payment",
            fields=[
                (
                    "payment_id",
                    models.UUIDField(
                        primary_key=True,
                        default=uuid.uuid4,
                        editable=False,
                        serialize=False,
                    ),
                ),
                ("stripe_payment_intent_id", models.CharField(max_length=255, unique=True)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("currency", models.CharField(default="USD", max_length=3)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("succeeded", "Succeeded"),
                            ("failed", "Failed"),
                            ("pending", "Pending"),
                            ("canceled", "Canceled"),
                        ],
                        max_length=20,
                    ),
                ),
                ("payment_method", models.CharField(blank=True, max_length=255, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "subscription",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="payments",
                        to="task_management.subscription",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="payments",
                        to="task_management.user",
                    ),
                ),
            ],
            options={"db_table": "payments", "ordering": ["-created_at"]},
        ),
    ]
