from __future__ import annotations

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import Email, User


class EmailAdminInline(admin.TabularInline):
    model = Email
    autocomplete_fields = [
        "user",
    ]


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = [
        "id",
        "avatar",
        "username",
        "is_active",
        "is_superuser",
        "is_staff",
    ]
    search_fields = [
        "id",
        "username",
        "first_name",
        "last_name",
    ]
    list_filter = [
        "is_active",
        "is_superuser",
        "is_staff",
    ]
    add_fieldsets = list(UserAdmin.add_fieldsets)
    add_fieldsets.append(
        (
            _("Extra"),
            {
                "fields": [
                    "birth_date",
                    "avatar",
                ]
            },
        ),
    )
    fieldsets = list(UserAdmin.fieldsets)
    fieldsets[0] = (
        _("User Info"),
        fieldsets[0][1],
    )
    fieldsets[1] = (  # type: ignore
        _("Personal Info"),
        {
            "fields": ("avatar", "birth_date", *fieldsets[1][1]["fields"]),
        },
    )
    inlines = [
        EmailAdminInline,
    ]
