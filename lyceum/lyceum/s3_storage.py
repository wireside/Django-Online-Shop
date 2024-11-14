from storages.backends.s3boto3 import S3Boto3Storage

__all__ = ["MediaStorage", "StaticStorage"]


class MediaStorage(S3Boto3Storage):
    bucket_name = "wireside-project-static-storage"
    location = "media"


class StaticStorage(S3Boto3Storage):
    bucket_name = "wireside-project-static-storage"
    location = "static"
