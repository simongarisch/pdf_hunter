"""
Some URLs ending with .pdf will need to be modified slightly.
We'll track each of these transformations in the UrlTransforms class.
"""


class UrlTransforms:
    _registry = []

    @classmethod
    def register(cls, func):
        cls._registry.append(func)
        return func

    @classmethod
    def apply(cls, url):
        for func in cls._registry:
            url = func(url)
        return url


@UrlTransforms.register
def modify_github_url(url):
    if url.startswith("https://github.com/"):
        return url.replace("/blob/", "/raw/")
    return url
