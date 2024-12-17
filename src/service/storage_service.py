from io import BytesIO

from minio import Minio
from src.config import minio_config
import uuid

client = Minio(
    endpoint=minio_config.minio_endpoint_url,
    access_key=minio_config.MINIO_ACCESS_KEY,
    secret_key=minio_config.MINIO_SECRET_KEY,
    secure=minio_config.MINIO_USE_SSL,
)

bucket_name = minio_config.MINIO_BUCKET

if not client.bucket_exists(bucket_name):
    client.make_bucket(bucket_name)
    print(f"Bucket '{bucket_name}' is ready.")


def upload_file(file_data: BytesIO, content_type: str) -> str:
    file_name = f"{uuid.uuid4()}.jpg"
    client.put_object(
        bucket_name=minio_config.MINIO_BUCKET,
        object_name=file_name,
        data=file_data,
        length=len(file_data.getvalue()),
        content_type=content_type,
    )
    url = client.get_presigned_url("GET", minio_config.MINIO_BUCKET, file_name)
    return url
