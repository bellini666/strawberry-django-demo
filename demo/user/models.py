from __future__ import annotations

from django.contrib.auth.models import AbstractUser
from django.db.models import ImageField
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Default user in the app."""

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    avatar = ImageField(
        verbose_name=_("Avatar"),
        max_length=2000,
        default=None,
        blank=True,
        null=True,
    )
