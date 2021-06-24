import requests
import os
from typing import List, Tuple
from tqdm import tqdm
import tarfile
import shutil
import logging
import sys

from app.service.package import create_item, clean_up
from app.schemas.package import PackageCreate
from app.schemas.developer import DeveloperCreate

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))

# python -m app.util.cran_data_util
ALL_PKG_URL = "https://cran.r-project.org/src/contrib/PACKAGES"


def url_for_a_package(name, version):
    return f"https://cran.r-project.org/src/contrib/{name}_{version}.tar.gz"


def get_a_number_of_package_name_and_version(number=3) -> List[Tuple[str, str]]:
    logger.info("Pulling all packages info...")
    r = requests.get(ALL_PKG_URL)
    contents = [x.strip() for x in r.text.split("\n")]
    found = 0
    packages = []
    versions = []
    for key_value_pair in contents:
        if "Package" in key_value_pair:
            packages.append(key_value_pair.split(": ")[1])
            found += 1
        if "Version" in key_value_pair:
            versions.append(key_value_pair.split(": ")[1])
            found += 1
        if found == 2 * number:
            break

    return [(x, y) for x, y in zip(packages, versions)]


def download_and_parse_package_desc(package: str, version: str) -> PackageCreate:
    logger.info(f"================ Download package: {package} ====================")
    tar_file_path = os.path.join(f"{package}.tar.gz")
    with requests.get(url=url_for_a_package(package, version), stream=True) as r:
        if r.status_code == 200:
            r.raise_for_status()
            total_size = int(r.headers.get("Content-Length", 0))
            chunk_size = 1024 * 64
            bar = tqdm(total=total_size, unit="iB", unit_scale=True)
            with open(tar_file_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=chunk_size):
                    bar.update(len(chunk))
                    f.write(chunk)
            bar.close()
            try:
                item_create = parse_desc(package=package, version=version)
                logger.warning(f"Parsing success!")
                return item_create
            except Exception as e:
                logger.warning(f"Parsing failed with exception: {str(e)}")
            finally:
                os.remove(tar_file_path)
                shutil.rmtree(package)
        else:
            logger.warning(f"Download failed for package {package}")


def parse_a_pair(key: str, value: str, package_data: dict) -> dict:
    if "Date/Publication" == key:
        package_data["publish_date"] = value.replace(" UTC", "+00:00").strip()
    elif "Title" == key:
        package_data["title"] = value.strip().replace("\n", "").replace("\t", "")
    elif "Description" == key:
        package_data["description"] = value.strip().replace("\n", "").replace("\t", "")
    elif "Author" == key:
        author_names = [x.split("[")[0].strip() for x in value.split(",")]
        author_names = list(set(author_names))
        package_data["authors"] = [{"name": x} for x in author_names]
    elif "Maintainer" == key:
        maintainer_names = [x.split("<")[0].strip() for x in value.split(",")]
        maintainer_names = list(set(maintainer_names))
        maintianer_emails = [
            x.split("<")[1].strip().strip(">") for x in value.split(",")
        ]
        package_data["maintainers"] = [
            {"name": x, "email": y} for x, y in zip(maintainer_names, maintianer_emails)
        ]
    return package_data


def parse_desc(package: str, version: str) -> PackageCreate:
    # unzip
    logger.info(f"Parsing package: {package}")
    tar_file_path = os.path.join(f"{package}.tar.gz")
    tar = tarfile.open(tar_file_path, "r:gz")
    tar.extractall()
    tar.close()

    # obtain the desc
    with open(os.path.join(package, "DESCRIPTION"), "r") as f:
        package_data = {
            "name": package,
            "version": version,
            "authors": [],
            "maintainers": [],
        }
        current_key = ""
        current_value = ""
        for line in f:
            if ": " in line:
                if current_key:
                    package_data = parse_a_pair(
                        current_key, current_value, package_data
                    )
                # restart the process
                current_key, current_value = line.split(": ", 1)
            else:
                current_value += line
        # do the last round
        package_data = parse_a_pair(current_key, current_value, package_data)
    return PackageCreate(**package_data)


def main(number=10):

    clean_up()
    package_infos = get_a_number_of_package_name_and_version(number=number)
    for p in package_infos:
        item_create = download_and_parse_package_desc(p[0], p[1])
        if item_create:
            print(item_create)
            create_item(item_create)


if __name__ == "__main__":
    # get_a_number_of_package_name_and_version()
    # download_package("abbyyR", "0.5.5")
    main(number=50)
