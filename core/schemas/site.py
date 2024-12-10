from enum import Enum
from pydantic import BaseModel


class Status(str, Enum):
    parsing_1 = "parsing_1"
    parsing_2 = "parsing_2"
    ok = "ok"
    error = "error"
    wait = "wait"


class SiteSchemas(BaseModel):
    url: str
    tag: str
    status: str = Status.wait.value
    progress: int = 0  # processing progress
    time_start: float = -1.0  # processing progress
    time_end: float = -1.0  # processing progress


class SiteUpdateSchemas(BaseModel):
    status: str | None = None
    progress: int | None = None  # processing progress
    time_start: float | None = None  # processing progress
    time_end: float | None = None  # processing progress
