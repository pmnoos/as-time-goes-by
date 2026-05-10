import boto3
import os
import uuid
import logging
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

R2_ACCOUNT_ID = os.getenv("R2_ACCOUNT_ID")
R2_ACCESS_KEY_ID = os.getenv("R2_ACCESS_KEY_ID")
R2_SECRET_ACCESS_KEY = os.getenv("R2_SECRET_ACCESS_KEY")
R2_BUCKET_NAME = os.getenv("R2_BUCKET_NAME")
R2_PUBLIC_URL = os.getenv("R2_PUBLIC_URL", "").rstrip("/")


def get_r2_client():
    return boto3.client(
        "s3",
        endpoint_url=f"https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com",
        aws_access_key_id=R2_ACCESS_KEY_ID,
        aws_secret_access_key=R2_SECRET_ACCESS_KEY,
        region_name="auto",
    )


def upload_image(file, filename: str) -> str | None:
    """
    Upload a file-like object to Cloudflare R2.
    Returns the public URL of the uploaded file, or None on failure.
    """
    try:
        suffix = Path(filename).suffix.lower()
        unique_name = f"uploads/{uuid.uuid4().hex}{suffix}"
        client = get_r2_client()
        client.upload_fileobj(
            file,
            R2_BUCKET_NAME,
            unique_name,
            ExtraArgs={"ContentType": _content_type(suffix)},
        )
        return f"{R2_PUBLIC_URL}/{unique_name}"
    except Exception as e:
        logging.error(f"R2 upload failed: {e}")
        return None


def delete_image(image_url: str) -> None:
    """
    Delete an image from Cloudflare R2 given its public URL.
    Silently ignores errors (e.g. file already deleted).
    """
    try:
        if not image_url or not R2_PUBLIC_URL:
            return
        key = image_url.replace(f"{R2_PUBLIC_URL}/", "")
        client = get_r2_client()
        client.delete_object(Bucket=R2_BUCKET_NAME, Key=key)
    except Exception as e:
        logging.error(f"R2 delete failed: {e}")


def _content_type(suffix: str) -> str:
    return {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".webp": "image/webp",
    }.get(suffix, "application/octet-stream")