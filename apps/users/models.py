from django.db import models
from django.contrib.auth.models import AbstractUser

from apps.utils.models import BaseModel
from .managers import UserManager

class User(AbstractUser, BaseModel):
    user_id = models.CharField(max_length=255, unique=True, db_index=True)
    phone = models.CharField(max_length=100, null=True, blank=True)

    objects = UserManager()
    REQUIRED_FIELDS = ["first_name", "last_name"]
    USERNAME_FIELD = "username"

    def __str__(self):
        return str(self.username)

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.user_id
        return super().save(*args, **kwargs)
    
    class Meta:
        db_table = "users"
        ordering = ["user_id"]