# from django.contrib.auth.models import AbstractUser
# from django.db import models

# class CustomUser(AbstractUser):
#     email = models.EmailField(unique=True)  # Email unique hona chahiye
#     role = models.CharField(max_length=50, choices=[('admin', 'Admin'), ('doctor', 'Doctor'), ('patient', 'Patient'), ('guardian', 'Guardian')], default='patient')

#     def __str__(self):
#         return self.username


# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
        ('guardian', 'Guardian'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='patient')

    def __str__(self):
        return self.username
