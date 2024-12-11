from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from celery_app import do_pars, pdf_pars_mistral
from core.database.site import SiteDB
from core.schemas.site import Status
from core.services.redis_client import get_redis, close_all_redis
from core.services.site_validator import PdfParser
from middleware import process_time_middleware, ErrorMiddleware
from routers import router as api_router

app = FastAPI(
    title="Valid Site App",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
)


@app.on_event("startup")
async def startup():
    site_db = SiteDB()
    r = get_redis(0)

    # try:
    #     pdf = PdfParser.get_pdf_stat()
    #     if pdf['status'] != "ok":
    #         path = pdf['path']
    #         pdf = PdfParser(path)
    #         pdf.run()
    #         pdf_pars_mistral.delay(pdf)
    # except Exception as e:
    #     print(e)


    all_sites = await site_db.get_all()

    for site in all_sites:
        r.set(site.tag, site.json())
        if site.status != Status.ok.value:
            do_pars.delay(site.url)


@app.on_event("shutdown")
async def shutdown():
    await close_all_redis()


app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_methods=['*'],
                   allow_headers=["*"],
                   allow_credentials=True, )

app.add_middleware(ErrorMiddleware)


@app.middleware('http')
async def process_time(request: Request, call_next):
    return await process_time_middleware(request, call_next)


app.include_router(api_router, prefix="/api")
