from fastapi import APIRouter
from .site import router as site_router
from .pdf import router as pdf_router
from .docs import router as docs_router

router = APIRouter(
    prefix="/v1"
)

router.include_router(site_router)
router.include_router(pdf_router)
router.include_router(docs_router)
