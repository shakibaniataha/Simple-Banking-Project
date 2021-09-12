from django.db import models
from rest_framework.exceptions import NotFound


class BaseModel(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    class Meta:
        abstract = True

    @classmethod
    def get_by_pk(cls, pk, raise_exception=False) -> 'BaseModel':
        obj = cls.objects.filter(pk=pk).first()
        if raise_exception and not obj:
            raise NotFound('The requested entity was not found.')

        return obj

    @classmethod
    def get_all(cls):
        return cls.objects.all()
