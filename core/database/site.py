from core.models.site import SiteModel
from core.schemas.site import SiteSchemas, SiteUpdateSchemas
from .database import get_session_async, get_session_sync
from sqlalchemy import select, update


class SiteDB:
    async def get(self, filters: dict) -> SiteSchemas:
        query = select(SiteModel).filter_by(**filters)
        async with get_session_async() as session:
            res = await session.execute(query)
            site = res.scalars().one_or_none()
            if site is None:
                return None

        return SiteSchemas.model_validate(site, from_attributes=True)

    async def get_all(self) -> list[SiteSchemas]:
        query = select(SiteModel)
        async with get_session_async() as session:
            res = await session.execute(query)
            sites = res.scalars().all()
            if sites is None:
                return []

        return [SiteSchemas.model_validate(site, from_attributes=True) for site in sites]

    async def update(self, url: str, site: SiteUpdateSchemas) -> bool:
        site = {key:val for key, val in site.dict().items() if val != None}
        query = update(SiteModel).where(SiteModel.url == url).values(**site)
        async with get_session_async() as session:
            try:
                await session.execute(query)
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e

        return True

    def update_sync(self, url: str, site: SiteUpdateSchemas) -> bool:
        site = {key:val for key, val in site.dict().items() if val != None}
        query = update(SiteModel).where(SiteModel.url == url).values(**site)
        with get_session_sync() as session:
            try:
                session.execute(query)
                session.commit()
            except Exception as e:
                session.rollback()
                raise e

        return True

    async def create(self, site: SiteSchemas) -> bool:
        site = SiteModel(**site.dict())
        async with get_session_async() as session:
            try:
                session.add(site)
                await session.commit()
                await session.refresh(site)
            except Exception as e:
                await session.rollback()
                raise e

        return True


