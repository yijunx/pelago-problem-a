from sqlalchemy.sql.expression import and_, or_
from app.schemas.pagination import ResponsePagination
from app.schemas.package import Package, PackageCreate, PackageWithPagination
from app.db import models
from sqlalchemy.orm import Session
from sqlalchemy import func
from uuid import uuid4


def create(db: Session, item_create: PackageCreate) -> models.Package:
    db_item = models.Package(
        id=str(uuid4()),
        name=item_create.name,
        version=item_create.version,
        publish_date=item_create.publish_date,
        title=item_create.title,
        description=item_create.description,
    )
    db.add(db_item)
    return db_item


def get_all(
    db: Session,
    author_id: str = None,
    maintainer_id: str = None,
    keyword: str = None,
    page: int = None,
    size: int = None,
) -> PackageWithPagination:

    query = db.query(models.Package)

    if author_id:
        query = query.filter(
            models.Package.authors.any(
                models.AuthorAssociation.developer_id == author_id
            )
        )

    if maintainer_id:
        query = query.filter(
            models.Package.maintainers.any(
                models.MaintainerAssociation.developer_id == maintainer_id
            )
        )

    if keyword:
        query = query.filter(
            or_(
                models.Package.description.ilike(f"%{keyword}%"),
                models.Package.title.ilike(f"%{keyword}%"),
            )
        )

    # pagination
    total = query.count()
    limit = size or total
    offset = (page - 1) * limit if page else 0
    current_page = page or 1
    total_pages = -(total // size) if size else 1

    db_items = query.limit(limit).offset(offset)
    items = [Package.from_orm(x) for x in db_items]

    paging = ResponsePagination(
        total=total,
        total_pages=total_pages,
        current_page=current_page,
        page_size=len(items),
    )
    return PackageWithPagination(data=items, paging=paging)


def get(db: Session, item_id) -> models.Package:
    return db.query(models.Package).filter(models.Package.id == item_id).first()


def delete(db: Session, item_id) -> None:
    db.query(models.Package).filter(models.Package.id == item_id).delete()


def delete_all(db: Session) -> None:
    db.query(models.Package).delete()
