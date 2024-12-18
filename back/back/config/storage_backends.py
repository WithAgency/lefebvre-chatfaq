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
    default_acl = "private"  # Set default ACL to 'private' for secure uploads
    file_overwrite = False    # Prevent files with the same name from being overwritten

    # Set to your Space's virtual-hosted style domain
    custom_domain = "lefebvre-chatfaq.ams3.digitaloceanspaces.com"

    # Define the signature version and region name as class attributes
    signature_version = 's3v4'  # Typically 's3v4' for DigitalOcean Spaces
    region_name = 'ams3'         # Your Space's region

    # ===============================
    # Initialization
    # ===============================

    def __init__(self, *args, **kwargs):
        """
        Initialize the storage backend with custom configurations for region and addressing style.
        """
        super().__init__(*args, **kwargs)

    # ===============================
    # Boto3 Client Configuration
    # ===============================

    def get_connection_params(self):
        """
        Override the connection parameters to set 'addressing_style' to 'virtual' and specify 'signature_version'.
        """
        params = super().get_connection_params()

        # Create a custom Config object with 'virtual' addressing style and 's3v4' signature version
        boto3_config = BotoConfig(
            signature_version='s3v4',
            s3={'addressing_style': 'virtual'}
        )

        # Update the existing 'config' in params if it exists, else add it
        if 'config' in params:
            # Merge existing s3 settings if any
            existing_s3 = params['config'].s3.copy() if 's3' in params['config'] else {}
            existing_s3.update({'addressing_style': 'virtual'})
            params['config'] = Config(
                signature_version='s3v4',
                s3=existing_s3
            )
        else:
            params['config'] = boto3_config

        return params

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
