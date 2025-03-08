from celery import shared_task
from django.utils.timezone import now
from .models import TemporaryRole

@shared_task
def revoke_expired_roles():
    expired_roles = TemporaryRole.objects.filter(expires_at__lte=now())
    for role in expired_roles:
        role.user.groups.remove(role.role)  # Role remove karein
        role.delete()  # Entry delete karein
