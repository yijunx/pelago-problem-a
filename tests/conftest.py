import pytest
from app.schemas.package import PackageCreate, PackageQuery
from app.schemas.developer import DeveloperCreate
from datetime import datetime


@pytest.fixture
def package_create(developer_1, developer_2):
    return PackageCreate(
        name="test-pkg",
        version="0.1.1",
        publish_date=datetime(2021, 7, 8),
        title="a test package",
        description="here is a long desc",
        authors=[developer_1, developer_2],
        maintainers=[developer_1],
    )


@pytest.fixture
def developer_1():
    return DeveloperCreate(name="yijun", email="yijun@x.com")


@pytest.fixture
def developer_2():
    return DeveloperCreate(name="erjun", email="erjun@x.com")
