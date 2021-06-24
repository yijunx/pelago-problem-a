from pydantic import BaseModel
from typing import Any, Optional


class StandardResponse(BaseModel):
    success: bool = True
    response: Any = None
    message: Optional[str]
