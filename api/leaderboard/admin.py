from django.contrib import admin
from .models import Group, Transaction


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("name", "public")


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("user", "amount", "description")
