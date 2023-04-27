import boto3
from botocore.exceptions import ClientError
from decouple import config


class S3Service:
    def __init__(self):
        self.s3 = boto3.resource(
            "s3",
            aws_access_key_id=config("AWS_ACCESS_KEY"),
            aws_secret_access_key=config("AWS_SECRET_KEY"),
        )

    def upload_file_pic(self, file_path, file_name, bucket=None, region=None):
        if not bucket:
            bucket = config("BUCKET_NAME")
        if not region:
            region = config("REGION_NAME")

        self.s3.meta.client.upload_file(file_path, bucket, file_name)

        return f"https://{bucket}.s3.{region}.amazonaws.com/{file_name}"

    def upload_file_pdf(self, file_path, file_name, bucket=None):
        if not bucket:
            bucket = config("BUCKET_NAME_INSURENCES")
        try:
            self.s3.meta.client.upload_file(file_path, bucket, file_name)
        except Exception as e:
            raise ClientError
