from django.contrib import admin

from core.models import Branch


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    pass
