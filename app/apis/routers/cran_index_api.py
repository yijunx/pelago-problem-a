from flask import Blueprint, Response, request
from flask_pydantic import validate
from app.service import photo as photoService
from app.schemas.photo import PhotoPatch, PhotoQuery, PhotoCreate
from app.util.requests_util import create_response


photo_bq = Blueprint("photo_bq", __name__)


@photo_bq.route("", methods=["GET"])
@validate(query=PhotoQuery)
def list_photos():
    item_query = request.query_params
    try:
        r = photoService.list_items(item_query=item_query)
    except:
        raise
    return create_response(
        response=r,
    )


@photo_bq.route("", methods=["POST"])
def post_photo():
    print("photo upload!")

    file = request.files.get("file")
    title = request.form.get("title")
    description = request.form.get("description", None)
    print("got file")

    item_create = PhotoCreate(title=title, description=description)

    try:
        r = photoService.create_item(item_create=item_create, file=file)
    except:
        raise

    return create_response(response=r)


@photo_bq.route("/<photo_id>", methods=["GET"])
def get_photo(photo_id: str):

    try:
        r = photoService.get_item(item_id=photo_id)
    except:
        raise
    return create_response(response=r)


@photo_bq.route("/<photo_id>/content", methods=["GET"])
def get_photo_content(photo_id: str):
    try:
        # look like need to store .xxx for each photo
        # as some file type...
        # here we dont return key, just name it photo-some random uid.type
        key, file = photoService.download_item(item_id=photo_id)
    except:
        raise

    return Response(
        file, headers={"Content-Disposition": f"attachment; filename={key}"}
    )


# @photo_bq.route("/<photo_id>/view", methods=["GET"])
# @validate(body=PhotoPatch)
# def get_photo_thumbnail(photo_id: str):
#     try:
#         r = photoService.patch_item(
#             item_id=photo_id, item_patch=request.body_params
#         )
#     except:
#         raise
#     return create_response(response=r)


@photo_bq.route("/<photo_id>", methods=["PATCH"])
@validate(body=PhotoPatch)
def update_photo(photo_id: str):
    try:
        r = photoService.patch_item(item_id=photo_id, item_patch=request.body_params)
    except:
        raise
    return create_response(response=r)


@photo_bq.route("/<photo_id>", methods=["DELETE"])
def delete_photo(photo_id: str):
    try:
        photoService.delete_item(item_id=photo_id)
    except:
        raise
    return create_response(message="Photo deleted")
