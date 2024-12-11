import json
from urllib.parse import urlparse

from fastapi import APIRouter, HTTPException, WebSocket, File, UploadFile

from celery_app import do_pars
from core.services.site_validator.tag import Tag
from core.services.redis_client import get_redis
from core.schemas.site import SiteSchemas, Status
from core.database.site import SiteDB

router = APIRouter(
    prefix="/pdf",
)

r = get_redis(0)
site_db = SiteDB()


@router.post("/")
async def add(pdf_file: UploadFile = File(...)):
    if not pdf_file.filename.endswith(".pdf"):
        raise HTTPException(400, detail="Supported only .pdf")



