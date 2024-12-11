import shutil

from fastapi import APIRouter, HTTPException, File, UploadFile

from celery_app import pdf_pars, celery
from core.database.site import SiteDB
from core.services.redis_client import get_redis
from core.services.site_validator import PdfParser

router = APIRouter(
    tags=['Pdf'],
    prefix="/pdf",
)

r = get_redis(0)
r3 = get_redis(3)
site_db = SiteDB()


@router.get("/status")
async def get_all_status():
    return {
        "ok": "Готово! Все стадии обработки пройдены",
        "ok_run_with_mistral": "Требования сформированы! Идет доп. обработка с помощью модели",
        "ok_without_mistral": "Требования сформированы",
        "run_without_mistral": "Сбор требований",
        "wait": "Ожидания начала парсинга",
    }



@router.post("/")
async def add(pdf_file: UploadFile = File(...)):
    if not pdf_file.filename.endswith(".pdf"):
        raise HTTPException(400, detail="Supported only .pdf")

    # Сохранение файла
    with open(pdf_file.filename, "wb") as buffer:
        shutil.copyfileobj(pdf_file.file, buffer)

    try:
        celery.control.revoke(r3.get(pdf_file.filename), terminate=True)
    except Exception as e:
        print(e)

    task = pdf_pars.delay(pdf_file.filename)
    r3.set(pdf_file.filename, task.id)

    return True


@router.get("/")
async def status():
    return PdfParser.get_pdf_stat()
