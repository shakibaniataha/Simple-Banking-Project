from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.models import Branch, BaseUserModel

admin.site.register(BaseUserModel, UserAdmin)


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    pass
