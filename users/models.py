from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    avatar = models.ImageField(default='anonimous.png')
    bio = models.TextField()
    phone_number = models.PhoneNumberField(_("phone number"), blank=True)
    is_teacher = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)