import json
from urllib.parse import urlparse

from fastapi import APIRouter, HTTPException, WebSocket
from celery_app import do_pars, celery
from core.database.site import SiteDB
from core.schemas.site import SiteSchemas, Status, SiteUpdateSchemas
from core.services.redis_client import get_redis
from core.services.site_validator import PdfParser
from core.services.site_validator.tag import Tag

router = APIRouter(
    tags=['Site'],
    prefix="/site",
)

r = get_redis(0)
r2 = get_redis(2)
site_db = SiteDB()


@router.get("/status")
async def get_all_status():
    return {
        Status.ok.value: "Готово",
        Status.parsing_1.value: "Основная стадия парсинга",
        Status.parsing_2.value: "Отчет готов. Идет вторя доп. стадия парсинга",
        Status.error.value: "Ошибка",
        Status.wait.value: "Ожидания начала парсинга",
    }


@router.post("/")
async def add(url: str):
    status = PdfParser.get_pdf_stat()['status']
    if "ok" not in status:
        raise HTTPException(403, detail=f"Pdf status is not ok; status: {status}")

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

    task = do_pars.delay(url)

    r2.set(tag, task.id)

    return True


@router.patch("/")
async def repars(url: str):
    status = PdfParser.get_pdf_stat()['status']
    if "ok" not in status:
        raise HTTPException(403, detail=f"Pdf status is not ok; status: {status}")

    url = urlparse(url)
    url = str(url.scheme + "://" + url.hostname)
    tag = Tag()(url)

    site_db = SiteUpdateSchemas(
        status=Status.wait.value,
        time_start=-1,  # processing progress
        time_end=-1,  # processing progress
    )

    site_r = SiteSchemas(
        url=url,
        tag=tag,
        status=Status.wait.value,
    )


    try:
        celery.control.revoke(r2.get(tag), terminate=True)
    except Exception as e:
        print(e)
    r.set(tag, site_r.json())
    await site_db.update(url, site_db)

    do_pars.delay(url)

    return True


@router.get("/", response_model=SiteSchemas)
async def get(url: str):
    try:
        return SiteSchemas(**json.loads(r.get(Tag()(url))))
    except:
        raise HTTPException(404, "Site does not exist")

@router.get("/all", response_model=list[SiteSchemas])
async def get_all_key():
    try:
        return [SiteSchemas(**json.loads(r.get(key))) for key in r.keys()]
    except:
        raise HTTPException(404, "Site does not exist")

@router.delete("/")
async def delete(url: str):
    try:
        url = urlparse(url)
        url = str(url.scheme + "://" + url.hostname)

        try:
            celery.control.revoke(r2.get(Tag()(url)), terminate=True)
        except Exception as e:
            print(e)

        r.delete(Tag()(url))
        await site_db.delete(url)
        return True
    except:
        raise HTTPException(404, "Site does not exist")


# @router.websocket("/")
# async def get_ws(url: str, websocket: WebSocket):
#     await websocket.accept()
#     while True:
#         try:
#             await websocket.send_text(SiteSchemas(**json.loads(r.get(Tag()(url)))))
#         except:
#             raise HTTPException(404, "Site does not exist")
