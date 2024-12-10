from fastapi import APIRouter
from .site import router as site_router

router = APIRouter(
    prefix="/v1"
)

router.include_router(site_router)
