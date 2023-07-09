from __future__ import annotations

import strawberry_django
from strawberry import relay

from .models import User


@strawberry_django.type(User, name="User")
class UserType(relay.Node):
    @strawberry_django.field(only=["first_name", "last_name"])
    def name(self, root: User) -> str:
        return f"{root.first_name} {root.last_name}".strip()

    @strawberry_django.field(only=["avatar"])
    def avatar(self, root: User) -> str | None:
        return root.avatar.url if root.avatar else None
