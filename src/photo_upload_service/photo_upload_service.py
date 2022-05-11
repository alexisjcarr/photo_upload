import os

import boto3
from botocore.exceptions import ClientError
from flask import Blueprint
import uuid
from sqlalchemy import BLOB


blueprint = Blueprint('photo_upload_service', __name__, url_prefix='/upload')


@blueprint.route('/', methods=['POST', 'GET'])
def upload(username, file_name, object_name=None):
    """
    Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')

    # TODO: create globally unique file name with uuid

    try:
        response = s3_client.upload_file(file_name, os.getenv('S3_BUCKET'), object_name)
        print(response)
    except ClientError as e:
        print(e)
        return False
    return True
