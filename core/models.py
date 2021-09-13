from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
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


class BaseUserModel(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    username = models.CharField(max_length=255, unique=True, validators=[username_validator],
                                error_messages={
                                    'unique': "A user with that username already exists.",
                                })
    USERNAME_FIELD = 'username'

    objects = UserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username


class Customer(models.Model):
    user = models.OneToOneField(BaseUserModel, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=255)


class Clerk(models.Model):
    user = models.OneToOneField(BaseUserModel, on_delete=models.CASCADE)


class Branch(BaseModel):
    name = models.CharField(max_length=255)
    clerk = models.OneToOneField(Clerk, on_delete=models.PROTECT, default=None)

    class Meta:
        verbose_name_plural = 'Branches'

    def __str__(self):
        return self.name
