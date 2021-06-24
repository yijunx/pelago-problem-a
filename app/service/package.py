from contextlib import contextmanager
from app.db.database import SessionLocal
from app.schemas.package import (
    PackageCreate,
    PackageQuery,
    Package,
    PackageWithPagination,
)
from app.repo import package as packageRepo
from app.repo import developer as developerRepo
from app.repo import author as authorRepo
from app.repo import maintainer as maintainerRepo


@contextmanager
def get_db():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def create_item(item_create: PackageCreate) -> Package:
    with get_db() as db:
        db_authors = developerRepo.batch_create(db=db, item_creates=item_create.authors)
        db_maintainers = developerRepo.batch_create(
            db=db, item_creates=item_create.maintainers
        )
        db_package = packageRepo.create(db=db, item_create=item_create)

        for db_developer in db_authors:
            authorRepo.create(db=db, db_package=db_package, db_developer=db_developer)
        for db_developer in db_maintainers:
            maintainerRepo.create(
                db=db, db_package=db_package, db_developer=db_developer
            )

        package = Package.from_orm(db_package)
    return package


def list_items(item_query: PackageQuery) -> PackageWithPagination:
    with get_db() as db:
        author_id = None
        if item_query.author_name:
            dev = developerRepo.get_by_name(db=db, item_name=item_query.author_name)
            if dev:
                author_id = dev.id

        maintainer_id = None
        if item_query.author_name:
            dev = developerRepo.get_by_name(db=db, item_name=item_query.maintainer_name)
            if dev:
                maintainer_id = dev.id

        packages_with_paging = packageRepo.get_all(
            db=db,
            author_id=author_id,
            maintainer_id=maintainer_id,
            keyword=item_query.keyword,
            page=item_query.page,
            size=item_query.size,
        )
    return packages_with_paging


def clean_up() -> None:
    with get_db() as db:
        authorRepo.delete_all(db=db)
        maintainerRepo.delete_all(db=db)
        packageRepo.delete_all(db=db)
        developerRepo.delete_all(db=db)
