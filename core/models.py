from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from datetime import timedelta
from rest_framework.exceptions import NotFound
from . import const
from decimal import Decimal


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


class Clerk(models.Model):
    user = models.OneToOneField(BaseUserModel, on_delete=models.CASCADE)


class Branch(BaseModel):
    name = models.CharField(max_length=255)
    clerk = models.OneToOneField(Clerk, on_delete=models.PROTECT, default=None)

    class Meta:
        verbose_name_plural = 'Branches'

    def __str__(self):
        return self.name


class Customer(models.Model):
    user = models.OneToOneField(BaseUserModel, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=255)

    @property
    def has_active_account(self):
        if hasattr(self, 'account') and self.account.is_active:
            return True

        return False
    
    def can_withdraw(self, amount):
        return bool(self.has_active_account and self.account.balance >= Decimal.from_float(float(amount)))
    
    def can_deposit(self):
        return self.has_active_account
    

class Account(BaseModel):
    # TODO: Create a uuid field to use for transactions

    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='accounts')
    is_active = models.BooleanField(default=True)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def close(self):
        self.is_active = False
        self.save()
        
    def withdraw(self, amount):
        self.balance -= Decimal.from_float(float(amount))
        self.save()

    def deposit(self, amount):
        self.balance += Decimal.from_float(float(amount))
        self.save()

    @property
    def username(self):
        return self.customer.user.username


class Transaction(BaseModel):
    from_account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='debits')
    to_account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='deposits')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    type = models.CharField(max_length=255, choices=const.TRANSACTION_TYPE_CHOICES)


class Loan(BaseModel):
    interest_rate = models.DecimalField(max_digits=4, decimal_places=2, default=0.2)
    annual_interest_rate = models.DecimalField(max_digits=4, decimal_places=2, default=0.1)
    amount = models.PositiveBigIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100000000)])
    type = models.CharField(max_length=255, choices=const.LOAN_TYPE_CHOICES, default=const.LOAN_TYPE_12_MONTHS)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='loans')
    returned_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    @property
    def due_date(self):
        return self.created_at + timedelta(int(self.type) / 12 * 365)
