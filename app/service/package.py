from contextlib import contextmanager
from app.db.database import SessionLocal
from typing import Tuple


@contextmanager
def get_db_session():

    session = SessionLocal()

    try:
        yield session
        session.commit()
    except:
        # also need to remove the data in the
        # data storage if possible
        session.rollback()
        raise
    finally:
        session.close()
