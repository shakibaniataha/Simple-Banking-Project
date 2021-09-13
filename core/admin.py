from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.models import Branch, BaseUserModel, Clerk

admin.site.register(BaseUserModel, UserAdmin)


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    pass


@admin.register(Clerk)
class ClerkAdmin(admin.ModelAdmin):
    pass
