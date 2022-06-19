from typing import Optional
from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    meguchan_url: str
