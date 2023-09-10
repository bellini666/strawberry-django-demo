from __future__ import annotations

import dataclasses
from typing import TYPE_CHECKING, Literal, cast, overload

from asgiref.sync import sync_to_async
from django.core.exceptions import PermissionDenied
from django.http.request import HttpRequest as _HttpRequest
from django.http.response import HttpResponse as _HttpResponse
from django.utils.translation import gettext_lazy as _
from strawberry.django.context import StrawberryDjangoContext
from strawberry.types import info

if TYPE_CHECKING:
    from typing import TypeAlias

    from django.contrib.auth.models import AnonymousUser
    from user.models import User

    from .dataloaders import DataLoaders


class HttpRequest(_HttpRequest):
    user: User | AnonymousUser


class HttpResponse(_HttpResponse):
    ...


@dataclasses.dataclass
class Context(StrawberryDjangoContext):
    request: HttpRequest
    response: HttpResponse | None
    dataloaders: DataLoaders

    @overload
    def get_user(self, *, required: Literal[True]) -> User:
        ...

    @overload
    def get_user(self, *, required: None = ...) -> User | None:
        ...

    def get_user(self, *, required: Literal[True] | None = None) -> User | None:
        user = self.request.user

        if not user or not user.is_authenticated or not user.is_active:
            if required:
                raise PermissionDenied(_("No user logged in"))

            return None

        return cast("User", user)

    @overload
    async def aget_user(self, *, required: Literal[True]) -> User:
        ...

    @overload
    async def aget_user(self, *, required: None = ...) -> User | None:
        ...

    async def aget_user(self, *, required: Literal[True] | None = None) -> User | None:
        return await sync_to_async(self.get_user)(required=required)


Info: TypeAlias = info.Info[Context, None]
