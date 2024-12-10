from urllib.parse import urlparse

from .redis_client import get_redis
from core.schemas.site import SiteSchemas, Status
import json

from ..RAG.tag import Tag

r = get_redis(0)

def set_site_progress(url: str, progress: int):
    url = urlparse(url)
    url = str(url.scheme + "://" + url.hostname)
    tag = Tag()(url)
    res = json.loads(r.get(tag))
    if res is None:
        raise Exception("Site not found")

    site = SiteSchemas(**res)

    site.progress = progress

    r.set(tag, site.json())
    return site


def set_site_status(url: str, status: Status):
    url = urlparse(url)
    url = str(url.scheme + "://" + url.hostname)
    tag = Tag()(url)
    res = json.loads(r.get(tag))
    if res is None:
        raise Exception("Site not found")

    site = SiteSchemas(**res)

    site.status = status.value

    r.set(tag, site.json())
    return site

def set_site_time_start(url: str, time: float):
    url = urlparse(url)
    url = str(url.scheme + "://" + url.hostname)
    tag = Tag()(url)
    res = json.loads(r.get(tag))
    if res is None:
        raise Exception("Site not found")

    site = SiteSchemas(**res)

    site.time_start = time

    r.set(tag, site.json())
    return site

def set_site_time_end(url: str, time: float):
    url = urlparse(url)
    url = str(url.scheme + "://" + url.hostname)
    tag = Tag()(url)
    res = json.loads(r.get(tag))
    if res is None:
        raise Exception("Site not found")

    site = SiteSchemas(**res)

    site.time_end = time

    r.set(tag, site.json())
    return site