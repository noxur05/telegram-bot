from django.db.models import QuerySet

class BaseQuerySet(QuerySet):
    def all(self):
        return super().all().filter(is_deleted=False)