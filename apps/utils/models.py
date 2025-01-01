from django.db import models

from .managers import BaseManager

class BaseModel(models.Model):
    date_created = models.DateTimeField(auto_now_add=True, db_index=True)
    date_updated = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False, db_index=True)

    objects = BaseManager()

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()
    
    class Meta:
        abstract = True
