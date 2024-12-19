import boto3
from botocore.config import Config

from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
from django.core.files.storage import FileSystemStorage


class PublicMediaS3Storage(S3Boto3Storage):
    default_acl = "public-read"
    file_overwrite = False


class PrivateMediaS3Storage(S3Boto3Storage):
    default_acl = "private"  # Set default ACL to 'private' for secure uploads
    file_overwrite = False  # Prevent files with the same name from being overwritten

    def generate_presigned_url(
        self,
        path: str,
        content_type: str = "application/octet-stream",
        expires_in: int = 3600,
    ):
        # # Create a session using DigitalOcean Spaces credentials
        # session = boto3.session.Session()

        # # Create S3 client with custom endpoint
        # s3_client = session.client(
        #     "s3",
        #     endpoint_url=settings.AWS_S3_CUSTOM_DOMAIN,
        #     aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        #     aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        #     config=Config(signature_version="s3v4"),
        # )

        # # Generate a signed URL for uploading
        # return s3_client.generate_presigned_url(
        #     "put_object",
        #     Params={
        #         "Bucket": settings.AWS_STORAGE_BUCKET_NAME,
        #         "Key": path,
        #         "ContentType": content_type,
        #         "ACL": self.default_acl,
        #     },
        #     ExpiresIn=expires_in,
        # )
        return self.connection.meta.client.generate_presigned_url(
            "put_object",
            Params={"Bucket": self.bucket_name, "Key": path, "ContentType": content_type},
            ExpiresIn=expires_in,
            HttpMethod="PUT",
        )


class PrivateMediaLocalStorage(FileSystemStorage):
    location = settings.MEDIA_ROOT


def select_private_storage():
    return (
        PrivateMediaLocalStorage()
        if settings.LOCAL_STORAGE
        else PrivateMediaS3Storage()
    )
