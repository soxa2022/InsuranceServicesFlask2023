import os
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import boto3
from botocore.exceptions import ClientError
from decouple import config

from constants import TEMP_FILE_FOLDER


class SES:
    def __init__(self):
        self.s3 = boto3.client(
            "s3",
            config("REGION_NAME"),
            aws_access_key_id=config("AWS_ACCESS_KEY"),
            aws_secret_access_key=config("AWS_SECRET_KEY"),
        )
        self.ses = boto3.client(
            "ses",
            config("REGION_NAME_SES"),
            aws_access_key_id=config("AWS_ACCESS_KEY"),
            aws_secret_access_key=config("AWS_SECRET_KEY"),
        )
        self.bucket_name = config("BUCKET_NAME_INSURENCES")
        self.path_file = os.path.join(TEMP_FILE_FOLDER, "policy_s3.pdf")

    def find_object_keys(self, file_name):
        response = self.s3.list_objects_v2(Bucket=self.bucket_name)
        file_key = None
        for obj in response.get("Contents", []):
            if obj["Key"].split("/")[-1] == file_name:
                file_key = obj["Key"]
                return file_key
        else:
            raise Exception(
                f"No file found with name {file_name} in bucket {self.bucket_name}"
            )

    def download_file(self, file_name):
        file_key = self.find_object_keys(file_name)
        self.s3.download_file(self.bucket_name, file_key, self.path_file)

    def send_mail(self, file_name, mail):  # create a message
        self.download_file(file_name)
        msg = MIMEMultipart()
        msg["From"] = mail
        msg["To"] = mail
        msg["Subject"] = "Your insurence policy from InsurenceServices"

        attachment = MIMEApplication(
            "Insurence policy", Name=os.path.basename(self.path_file)
        )
        attachment[
            "Content-Disposition"
        ] = f'attachment; filename="{os.path.basename(self.path_file)}"'
        msg.attach(attachment)
        msg.attach(MIMEText("Test email with attachment"))

        try:
            response = self.ses.send_raw_email(
                Source=mail, Destinations=[mail], RawMessage={"Data": msg.as_string()}
            )

        except Exception as e:
            raise ClientError
        else:
            return response["MessageId"]
