from sqlalchemy.sql.expression import and_, or_
from app.schemas.pagination import ResponsePagination
from app.db import models
from sqlalchemy.orm import Session
from uuid import uuid4


def create(
    db: Session, db_package: models.Package, db_developer: models.Developer
) -> models.MaintainerAssociation:
    db_item = models.MaintainerAssociation(id=str(uuid4()))
    db_item.package = db_package
    db_item.developer = db_developer
    db.add(db_item)
    return db_item


def delete_all(db: Session) -> None:
    db.query(models.MaintainerAssociation).delete()


def delete(db: Session, item_id: str) -> None:
    db.query(models.MaintainerAssociation).filter(
        models.MaintainerAssociation.id == item_id
    ).delete()


def get(db: Session, item_id: str) -> models.MaintainerAssociation:
    return (
        db.query(models.MaintainerAssociation)
        .filter(models.MaintainerAssociation.id == item_id)
        .first()
    )
