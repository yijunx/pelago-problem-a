from app.schemas.pagination import QueryPagination, ResponsePagination
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .developer import Developer


class PackageCreate(BaseModel):
    name: str
    version: str
    publish_date: datetime
    title: str
    description: str
    
    authors: List[Developer]
    maintainers: List[Developer]


class Package(PackageCreate):
    id: str

    class Config:
        orm_mode = True


class PackageWithPagination(BaseModel):
    data: List[Package]
    paging: ResponsePagination