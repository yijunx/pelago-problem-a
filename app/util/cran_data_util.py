import requests
import os
from typing import List, Tuple
from tqdm import tqdm
# from app.service.package import create_item, clean_up
# from app.schemas.package import PackageCreate
import tarfile


ALL_PKG_URL = "https://cran.r-project.org/src/contrib/PACKAGES"


def url_for_a_package(name, version):
    return f"https://cran.r-project.org/src/contrib/{name}_{version}.tar.gz"


def get_a_number_of_package_name_and_version(number=3) -> List[Tuple[str, str]]:
    r = requests.get(ALL_PKG_URL)
    contents = [x.strip() for x in r.text.split('\n')]
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


def download_and_unzip_to_get_desc(package, version):
    tar_file_path = os.path.join("downloads", f"{package}.tar.gz")
    with requests.get(
        url=url_for_a_package(package, version),
        stream=True
    ) as r:
        r.raise_for_status()
        total_size = int(r.headers.get("Content-Length", 0))
        chunk_size = 1024 * 64
        bar = tqdm(total=total_size, unit="iB", unit_scale=True)
        with open(tar_file_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=chunk_size):
                bar.update(len(chunk))
                f.write(chunk)
        bar.close
    
    # unzip
    tar = tarfile.open(tar_file_path, "r:gz")
    tar.extractall()
    tar.close()

    # delete
    os.remove(tar_file_path)





def prepare_data_and_save_to_db():



    return


# def cleanup_db():
#     clean_up()


if __name__ == '__main__':
    # get_a_number_of_package_name_and_version()
    download_and_unzip_to_get_desc("A3", "1.0.0")