from urllib.parse import urlparse

import idna


class Tag:
    def __call__(self, url: str):
        return idna.decode(urlparse(url).hostname)
