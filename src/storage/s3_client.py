# src/storage/s3_client.py
import os

import boto3
from botocore.exceptions import ClientError


class S3Client:
    """boto3 wrapper for S3 upload, download, and existence checks."""

    def __init__(self, bucket_name: str):
        """Initialize S3 client with bucket name and region from environment."""
        self.bucket_name = bucket_name
        self.client = boto3.client("s3", region_name=os.getenv("AWS_REGION_NAME"))

    def upload_file(self, local_path: str, s3_key: str) -> None:
        """Upload a local file to S3."""
        self.client.upload_file(local_path, self.bucket_name, s3_key)

    def download_file(self, s3_key: str, local_path: str) -> None:
        """Download an S3 object to a local path."""
        self.client.download_file(self.bucket_name, s3_key, local_path)

    def file_exists(self, s3_key: str) -> bool:
        """Return True if the object exists in the bucket, False if 404, raise otherwise."""
        try:
            self.client.head_object(Bucket=self.bucket_name, Key=s3_key)
            return True
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                return False
            raise
