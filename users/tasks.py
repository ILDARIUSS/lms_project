from datetime import timedelta

from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone


User = get_user_model()


@shared_task
def deactivate_inactive_users():
    threshold_date = timezone.now() - timedelta(days=30)

    users_to_deactivate = User.objects.filter(
        is_active=True,
        is_superuser=False,
        last_login__isnull=False,
        last_login__lt=threshold_date,
    )

    count = users_to_deactivate.update(is_active=False)

    return f'Deactivated users: {count}'