from django.contrib.auth.base_user import AbstractBaseUser
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


class BaseUserModel(AbstractBaseUser):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    USERNAME_FIELD = 'username'

    class Meta:
        abstract = True

    def __str__(self):
        return self.username

    @property
    def is_customer(self):
        return False

    @property
    def is_clerk(self):
        return False


class Customer(BaseUserModel):
    @property
    def is_customer(self):
        return True


class Clerk(BaseUserModel):
    @property
    def is_clerk(self):
        return True


class Branch(BaseModel):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Branches'

    def __str__(self):
        return self.name
