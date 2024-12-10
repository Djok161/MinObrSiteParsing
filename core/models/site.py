from sqlalchemy.orm import Mapped, mapped_column

from core.database.database import Base


class SiteModel(Base):
    __tablename__ = 'sites'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    url: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)
    tag: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)
    status: Mapped[str] = mapped_column(nullable=False)
    progress: Mapped[int] = mapped_column(nullable=False, default=0)
    time_start: Mapped[float] = mapped_column(nullable=False, default=-1.0)  # processing progress
    time_end: Mapped[float] = mapped_column(nullable=False, default=-1.0)  # processing progress
