from django.db.models.manager import Manager
from .querysets import BaseQuerySet

class BaseManager(Manager.from_queryset(BaseQuerySet)):
    def get_queryset(self):
        return super().get_queryset()