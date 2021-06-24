from pydantic.errors import NoneIsAllowedError
from sqlalchemy.sql.expression import and_, or_
from app.schemas.pagination import ResponsePagination
from app.schemas.developer import DeveloperCreate, Developer, DeveloperWithPagination
from app.db import models
from sqlalchemy.orm import Session
from uuid import uuid4
from typing import List


def create(db: Session, item_create: DeveloperCreate) -> models.Developer:
    db_item = models.Developer(
        id=str(uuid4()), name=item_create.name, email=item_create.email
    )
    db.add(db_item)
    return db_item


def get(db: Session, item_id: str) -> models.Developer:
    return db.query(models.Developer).filter(models.Developer.id == item_id).first()


def delete(db: Session, item_id: str) -> None:
    db.query(models.Developer).filter(models.Developer.id == item_id).delete()


def get_by_name(db: Session, item_name: str) -> models.Developer:
    return db.query(models.Developer).filter(models.Developer.name == item_name).first()


def delete_all(db: Session) -> None:
    db.query(models.Developer).delete()


def batch_create(
    db: Session, item_creates: List[DeveloperCreate]
) -> List[models.Developer]:
    db_items = []
    for item_create in item_creates:
        db_item = get_by_name(db=db, item_mame=item_create.name)
        if db_item is None:
            db_item = create(db=db, item_create=item_create)
        # update email if possible
        db_item.email = item_create.email or db_item.email
        db_items.append(db_item)
