from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    email = models.CharField(unique=True,max_length=100)
    phone = models.CharField(unique=True,max_length=12)

    def __str__(self):
        return self.username
