from sqlalchemy import Column, String, DateTime, UniqueConstraint
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Package(Base):
    __tablename__ = "packages"

    id = Column(String, primary_key=True, index=True)

    name = Column(String, nullable=False)
    version = Column(String, nullable=False)
    publish_date = Column(DateTime, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)

    authors = relationship("AuthorAssociation", back_populates="package")
    maintainers = relationship("MaintainerAssociation", back_populates="package")


class Developer(Base):
    __tablename__ = "developers"

    id = Column(String, primary_key=True, index=True)

    name = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=True)


class AuthorAssociation(Base):
    __tablename__ = "authorassociations"
    __table_args__ = (
        UniqueConstraint(
            "developer_id", "package_id", name="_developer_package_for_author_uc"
        ),
    )
    id = Column(String, primary_key=True, index=True)

    developer_id = Column(String, ForeignKey("developers.id"), nullable=False)
    package_id = Column(String, ForeignKey("packages.id"), nullable=False)

    package = relationship("Package", back_populates="authors")
    developer = relationship("Developer", back_populates="packages")


class MaintainerAssociation(Base):
    __tablename__ = "maintainerassociations"
    __table_args__ = (
        UniqueConstraint(
            "developer_id", "package_id", name="_developer_package_for_maintainer_uc"
        ),
    )

    id = Column(String, primary_key=True, index=True)

    developer_id = Column(String, ForeignKey("developers.id"), nullable=False)
    package_id = Column(String, ForeignKey("packages.id"), nullable=False)

    package = relationship("Package", back_populates="authors")
    developer = relationship("Developer", back_populates="packages")
