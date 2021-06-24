from app.schemas.pagination import QueryPagination, ResponsePagination
from pydantic import BaseModel
from typing import List, Optional


class DeveloperCreate(BaseModel):
    name: str
    email: Optional[str]


class Developer(DeveloperCreate):
    id: str

    class Config:
        orm_mode = True


class DeveloperWithPagination(BaseModel):
    data: List[Developer]
    paging: ResponsePagination
