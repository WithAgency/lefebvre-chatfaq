import re

from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
from botocore.client import Config as BotoConfig  # Import Config with alias to avoid confusion
from django.core.files.storage import FileSystemStorage


def transform_url(url):
    # Extract the bucket name and region
    match = re.search(r'https://([^.]+)\.digitaloceanspaces\.com/([^/]+)', url)
    if match:
        region = match.group(1)
        bucket_name = match.group(2)

        # Replace the beginning of the URL
        new_url = re.sub(
            f'https://{region}.digitaloceanspaces.com/{bucket_name}',
            f'https://{bucket_name}.{region}.digitaloceanspaces.com',
            url
        )

        return new_url
    else:
        return url  # Return original URL if pattern doesn't match

class PublicMediaS3Storage(S3Boto3Storage):
    default_acl = "public-read"
    file_overwrite = False


class PrivateMediaS3Storage(S3Boto3Storage):
    default_acl = "private"
    file_overwrite = False
    custom_domain = "lefebvre-chatfaq.ams3.digitaloceanspaces.com"  # Set to virtual-hosted domain

    def __init__(self, *args, **kwargs):
        """
        Initialize the storage backend with custom configurations for region and addressing style.
        """
        # Create a custom Config object with 'virtual' addressing style and 's3v4' signature version
        boto3_config = BotoConfig(
            signature_version='s3v4',
            s3={'addressing_style': 'virtual'}         # Enforce virtual-hosted style URLs
        )

        # Update the kwargs with the custom domain and config
        kwargs.update({
            'custom_domain': self.custom_domain,
            'config': boto3_config,
            'region_name': self.region_name,  # Ensure 'region_name' is set in your environment or here
        })

        super().__init__(*args, **kwargs)

    def generate_presigned_url(self, path, content_type, expires_in=3600):
        """
        Generate a presigned URL for a PUT request to the given path and content type.
        Expires in 2 hours by default.
        """
        url = self.connection.meta.client.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": self.bucket_name,
                "Key": path,
                "ContentType": content_type,
                'ACL': self.default_acl
            },
            ExpiresIn=expires_in,
            HttpMethod="PUT",
        )
        return url

class PrivateMediaLocalStorage(FileSystemStorage):
    location = settings.MEDIA_ROOT


def select_private_storage():
    return PrivateMediaLocalStorage() if settings.LOCAL_STORAGE else PrivateMediaS3Storage()
