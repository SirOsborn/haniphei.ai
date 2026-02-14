import asyncio
import os
import uuid
import logging
from datetime import datetime
from typing import Optional, Tuple
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

from api.core.config import settings

logger = logging.getLogger(__name__)


class StorageService:
    def __init__(self):
        self.bucket_name = settings.s3_bucket_name
        self.region = settings.s3_region
        self.s3_client = self._create_s3_client()

    def _create_s3_client(self):
        config = Config(
            region_name=self.region,
            signature_version="s3v4",
            retries={"max_attempts": 3, "mode": "standard"},
        )

        # Build client kwargs
        client_kwargs = {"config": config}

        # Add custom endpoint URL if provided (for R2, MinIO, Railway, etc.)
        if settings.s3_endpoint_url:
            client_kwargs["endpoint_url"] = settings.s3_endpoint_url  # type: ignore

        # Prefer IAM roles (ECS/EC2/Lambda). Only use static keys if you must.
        if getattr(settings, "s3_access_key_id", None) and getattr(settings, "s3_secret_access_key", None):
            client_kwargs["aws_access_key_id"] = settings.s3_access_key_id  # type: ignore
            client_kwargs["aws_secret_access_key"] = settings.s3_secret_access_key  # type: ignore

        return boto3.client("s3", **client_kwargs)

    @staticmethod
    def _safe_filename(filename: str) -> str:
        # Remove any directory components and keep a simple name
        base = os.path.basename(filename).strip()
        return base or "file"

    def _make_key(self, user_id: str, filename: str) -> str:
        ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        safe = self._safe_filename(filename)
        suffix = uuid.uuid4().hex[:12]
        return f"documents/{user_id}/{ts}_{suffix}_{safe}"

    async def upload_file(
        self,
        file_content: bytes,
        user_id: str,
        filename: str,
        content_type: str,
        *,
        metadata: Optional[dict] = None,
        kms_key_id: Optional[str] = None,
    ) -> Tuple[str, str]:
        """
        Uploads an object and returns (s3_key, presigned_get_url).
        By default uses SSE-S3 (AES256). Optionally supports SSE-KMS.
        """
        s3_key = self._make_key(user_id, filename)

        put_kwargs = {
            "Bucket": self.bucket_name,
            "Key": s3_key,
            "Body": file_content,
            "ContentType": content_type,
            "Metadata": metadata or {},
            # Better for common "download" UX (optional):
            "ContentDisposition": f'inline; filename="{self._safe_filename(filename)}"',
        }

        # Encryption
        if kms_key_id:
            put_kwargs["ServerSideEncryption"] = "aws:kms"
            put_kwargs["SSEKMSKeyId"] = kms_key_id
        else:
            put_kwargs["ServerSideEncryption"] = "AES256"

        try:
            await asyncio.to_thread(self.s3_client.put_object, **put_kwargs)

            # Return a presigned URL rather than a "public URL"
            url = await self.get_file_url(s3_key, expires_in=3600)

            logger.info("File uploaded successfully: %s", s3_key)
            return s3_key, url

        except ClientError:
            logger.exception("Error uploading file to S3 (key=%s)", s3_key)
            raise

    async def delete_file(self, s3_key: str) -> bool:
        try:
            await asyncio.to_thread(
                self.s3_client.delete_object,
                Bucket=self.bucket_name,
                Key=s3_key,
            )
            logger.info("File deleted successfully: %s", s3_key)
            return True

        except ClientError:
            logger.exception("Error deleting file from S3 (key=%s)", s3_key)
            raise

    async def get_file_url(self, s3_key: str, expires_in: int = 3600) -> str:
        try:
            return await asyncio.to_thread(
                self.s3_client.generate_presigned_url,
                "get_object",
                Params={"Bucket": self.bucket_name, "Key": s3_key},
                ExpiresIn=expires_in,
            )
        except ClientError:
            logger.exception("Error generating presigned URL (key=%s)", s3_key)
            raise


storage_service = StorageService()
