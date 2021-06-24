from flask import Blueprint, Response, request
from flask_pydantic import validate
from app.schemas.package import PackageCreate, PackageQuery
from app.util.requests_util import create_response
from app.service.package import list_items, create_item, get_item


cran_index_bp = Blueprint("cran_index_bp", __name__)


@cran_index_bp.route("", methods=["GET"])
@validate(query=PackageQuery)
def list_packages():
    try:
        r = list_items(item_query=request.query_params)
    except Exception as e:
        return create_response(response=None, success=False, message=str(e)), 500
    return create_response(response=r)


@cran_index_bp.route("/<package_id>", methods=["GET"])
@validate(query=PackageQuery)
def get_a_package(package_id: str):
    try:
        r = get_item(item_id=package_id)
    except Exception as e:
        return create_response(response=None, success=False, message=str(e)), 500
    return create_response(response=r)


@cran_index_bp.route("", methods=["POST"])
@validate(body=PackageCreate)
def post_package():
    item_create = request.body_params
    try:
        r = create_item(item_create=item_create)
    except Exception as e:
        return create_response(response=None, success=False, message=str(e)), 500
    return create_response(response=r, message="package created")
