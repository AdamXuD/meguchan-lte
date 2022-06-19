from typing import Optional
from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    meguchan_api: str
    meguchan_url: str
    meguchan_secret: Optional[str] = None
