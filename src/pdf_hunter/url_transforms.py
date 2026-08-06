"""
Some URLs ending with .pdf will need to be modified slightly.
We'll track each of these transformations in the UrlTransforms class.
"""

from collections.abc import Callable
from typing import ClassVar


class UrlTransforms:
    _registry: ClassVar[list] = []

    @classmethod
    def register(cls, func: Callable) -> Callable:
        cls._registry.append(func)
        return func

    @classmethod
    def apply(cls, url: str) -> str:
        for func in cls._registry:
            url = func(url)
        return url


@UrlTransforms.register
def modify_github_url(url: str) -> str:
    if url.startswith("https://github.com/"):
        return url.replace("/blob/", "/raw/")
    return url
