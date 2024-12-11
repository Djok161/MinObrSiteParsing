import json
from urllib.parse import urlparse

from fastapi import APIRouter, HTTPException, WebSocket

from celery_app import do_pars
from core.services.site_validator.tag import Tag
from core.services.redis_client import get_redis
from core.schemas.site import SiteSchemas, Status
from core.database.site import SiteDB

router = APIRouter(
    prefix="/site",
)

r = get_redis(0)
site_db = SiteDB()


@router.post("/")
async def add(url: str):
    url = urlparse(url)
    url = str(url.scheme + "://" + url.hostname)
    tag = Tag()(url)

    if tag in r.keys():
        raise HTTPException(403, "Site already exists")

    site = SiteSchemas(
        url=url,
        tag=tag,
        status=Status.wait.value,
    )

    r.set(tag, site.json())
    await site_db.create(site)

    do_pars.delay(url)

    return True


@router.get("/", response_model=SiteSchemas)
async def get(url: str):
    try:
        return SiteSchemas(**json.loads(r.get(Tag()(url))))
    except:
        raise HTTPException(404, "Site does not exist")

@router.websocket("/")
async def get_ws(url: str, websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            await websocket.send_text(SiteSchemas(**json.loads(r.get(Tag()(url)))))
        except:
            raise HTTPException(404, "Site does not exist")

