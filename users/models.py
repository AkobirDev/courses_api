from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

class CustomUser(AbstractUser):
    avatar = models.ImageField(default='anonimous.png')
    bio = models.TextField()
    phone_number = PhoneNumberField(_("phone number"), blank=True)
    is_teacher = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)