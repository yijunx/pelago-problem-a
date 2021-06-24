from app.schemas.package import Package, PackageWithPagination, PackageCreate
from app.service.package import clean_up


def test_create_item(client, package_create_json: dict):
    r = client.post(f"api/packages", json=package_create_json)
    print(r.get_json())
    package = Package(**r.get_json()["response"])
    assert package.title == package_create_json["title"]


def test_search_item(client, package_create: PackageCreate):
    r = client.get(f"api/packages?author_name=yijunx")
    packages = PackageWithPagination(**r.get_json()["response"])
    assert packages.data[0].title == package_create.title


def test_cleanup():
    clean_up()
