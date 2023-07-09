from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from strawberry.dataloader import DataLoader

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable, Sequence

_K = TypeVar("_K")
_T = TypeVar("_T")


class DataLoaders:
    def __init__(self):
        super().__init__()
        self._loaders: dict[Callable, DataLoader] = {}

    def __getitem__(
        self,
        key: Callable[[list[_K]], Awaitable[Sequence[_T | BaseException]]],
    ) -> DataLoader[_K, _T]:
        loader = self._loaders.get(key)
        if loader is None:
            loader = DataLoader(key)
            self._loaders[key] = loader

        return loader

    def clear(self):
        for loader in self._loaders.values():
            loader.clear_all()
