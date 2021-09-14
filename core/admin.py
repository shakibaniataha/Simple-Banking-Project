from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.models import Branch, BaseUserModel, Clerk, Account, Customer, Transaction, Loan

admin.site.register(BaseUserModel, UserAdmin)


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    pass


@admin.register(Clerk)
class ClerkAdmin(admin.ModelAdmin):
    pass


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    pass


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    pass


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    pass
