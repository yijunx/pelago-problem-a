from sqlalchemy.sql.expression import and_, or_
from app.schemas.pagination import ResponsePagination
from app.schemas.developer import DeveloperCreate, Developer, DeveloperWithPagination
from app.db import models
from sqlalchemy.orm import Session
from uuid import uuid4


def create(db: Session, item_create: DeveloperCreate) -> models.Developer:
    db_item = models.Developer(
        id=str(uuid4()), name=item_create.name, email=item_create.email
    )
    db.add(db_item)
    return db_item


def delete():
    return


def delete_all():
    return
