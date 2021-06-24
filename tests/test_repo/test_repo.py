from app.repo import package as packageRepo
from app.repo import developer as developerRepo
from app.repo import author as authorRepo
from app.repo import maintainer as maintainerRepo
from app.schemas.developer import DeveloperCreate
from app.schemas.package import PackageCreate
from sqlalchemy.orm import Session


PACKAGE_ID = ""
DEV_ID_1 = ""
DEV_ID_2 = ""
AUTHOR_ID = ""
MAINTAINER_ID = ""


def test_create_developer(db: Session, developer_1: DeveloperCreate):
    db_dev = developerRepo.create(db=db, item_create=developer_1)
    global DEV_ID_1
    DEV_ID_1 = db_dev.id
    assert db_dev.name == developer_1.name
    assert db_dev.email == developer_1.email


def test_get_developer(db: Session, developer_1: DeveloperCreate):
    db_dev = developerRepo.get(db=db, item_id=DEV_ID_1)
    assert db_dev.name == developer_1.name
    db_dev = developerRepo.get_by_name(db=db, item_name=developer_1.name)
    assert db_dev.id == DEV_ID_1


def test_create_package(db: Session, package_create: PackageCreate):
    db_pac = packageRepo.create(db=db, item_create=package_create)
    global PACKAGE_ID
    PACKAGE_ID = db_pac.id
    assert db_pac.description == package_create.description


def test_create_author(db: Session):
    db_pac = packageRepo.get(db=db, item_id=PACKAGE_ID)
    db_dev = developerRepo.get(db=db, item_id=DEV_ID_1)
    db_aut = authorRepo.create(db=db, db_developer=db_dev, db_package=db_pac)
    global AUTHOR_ID
    AUTHOR_ID = db_aut.id


def test_create_maintainer(db: Session):
    db_pac = packageRepo.get(db=db, item_id=PACKAGE_ID)
    db_dev = developerRepo.get(db=db, item_id=DEV_ID_1)
    db_mai = maintainerRepo.create(db=db, db_developer=db_dev, db_package=db_pac)
    global MAINTAINER_ID
    MAINTAINER_ID = db_mai.id


def test_get_author_and_maintainer(db: Session):
    db_aut = authorRepo.get(db=db, item_id=AUTHOR_ID)
    assert db_aut.package_id == PACKAGE_ID
    assert db_aut.developer_id == DEV_ID_1
    db_mai = maintainerRepo.get(db=db, item_id=MAINTAINER_ID)
    assert db_mai.package_id == PACKAGE_ID
    assert db_mai.developer_id == DEV_ID_1


def test_search_package_via_keyword(db: Session):
    packages_with_paging = packageRepo.get_all(db=db, keyword="here")
    assert packages_with_paging.data[0].id == PACKAGE_ID
    packages_with_paging = packageRepo.get_all(db=db, keyword="test")
    assert packages_with_paging.data[0].id == PACKAGE_ID


def test_search_package_via_author_id(db: Session):
    packages_with_paging = packageRepo.get_all(db=db, author_id=DEV_ID_1)
    assert packages_with_paging.data[0].id == PACKAGE_ID


def test_search_package_via_maintainer_id(db: Session):
    packages_with_paging = packageRepo.get_all(db=db, maintainer_id=DEV_ID_1)
    assert packages_with_paging.data[0].id == PACKAGE_ID


def test_delete_author(db: Session):
    authorRepo.delete(db=db, item_id=AUTHOR_ID)


def test_delete_maintainer(db: Session):
    maintainerRepo.delete(db=db, item_id=MAINTAINER_ID)


def test_delete_package(db: Session):
    packageRepo.delete(db=db, item_id=PACKAGE_ID)
    db_pac = packageRepo.get(db=db, item_id=PACKAGE_ID)
    assert db_pac == None


def test_delete_developer(db: Session):
    developerRepo.delete(db=db, item_id=DEV_ID_1)
    db_dev = developerRepo.get(db=db, item_id=DEV_ID_1)
    assert db_dev == None
