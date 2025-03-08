# from django.contrib.auth.models import AbstractUser
# from django.db import models

# class CustomUser(AbstractUser):
#     email = models.EmailField(unique=True)  # Email unique hona chahiye
#     role = models.CharField(max_length=50, choices=[('admin', 'Admin'), ('doctor', 'Doctor'), ('patient', 'Patient'), ('guardian', 'Guardian')], default='patient')

#     def __str__(self):
#         return self.username


# Create your models here.
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.utils.timezone import now, timedelta

class TemporaryRole(models.Model):
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.ForeignKey(Group, on_delete=models.CASCADE)  
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="assigned_roles", on_delete=models.CASCADE)  # ✅ FIXED!

    start_time = models.DateTimeField(default=now)
    duration = models.DurationField()  # Example: 2 hours, 1 day, etc.
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = self.start_time + self.duration
        super().save(*args, **kwargs)

    def is_expired(self):
        return now() >= self.expires_at

    def __str__(self):
        return f"{self.user} as {self.role} (Expires: {self.expires_at})"


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('super_admin', 'Super Admin'),

        ('admin', 'Admin'),
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
        ('guardian', 'Guardian'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='patient')

    def __str__(self):
        return self.username
