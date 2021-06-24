from app.schemas.pagination import QueryPagination, ResponsePagination
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .developer import Developer, DeveloperCreate


class PackageCreate(BaseModel):
    name: str
    version: str
    publish_date: datetime
    title: str
    description: str

    authors: List[DeveloperCreate]
    maintainers: List[DeveloperCreate]


class Package(BaseModel):
    id: str
    name: str
    version: str
    publish_date: datetime
    title: str
    description: str

    class Config:
        orm_mode = True


class PackageWithDevelopers(Package):
    authors: List[Developer]
    maintainers: List[Developer]


class PackageWithPagination(BaseModel):
    data: List[Package]
    paging: ResponsePagination


class PackageQuery(QueryPagination):
    keyword: Optional[str]
    author_name: Optional[str]
    maintainer_name: Optional[str]
