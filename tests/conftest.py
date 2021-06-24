import pytest
from app.schemas.package import PackageCreate
from app.schemas.developer import DeveloperCreate
from datetime import datetime, timezone


@pytest.fixture
def package_create_json(developer_1_json, developer_2_json):
    return {
        "name": "test-pkg",
        "version": "0.1.1",
        "publish_date": "2021-03-19T15:14:13",
        "title": "a test package",
        "description": "here is a long desc",
        "authors": [developer_1_json, developer_2_json],
        "maintainers": [developer_1_json],
    }


@pytest.fixture
def developer_1_json():
    return {"name": "yijun", "email": "yijun@x.com"}


@pytest.fixture
def developer_2_json():
    return {"name": "erjun", "email": "erjun@x.com"}


@pytest.fixture
def package_create(package_create_json):
    return PackageCreate(**package_create_json)


@pytest.fixture
def developer_1(developer_1_json):
    return DeveloperCreate(**developer_1_json)


@pytest.fixture
def developer_1(developer_2_json):
    return DeveloperCreate(**developer_2_json)
