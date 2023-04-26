import os

from constants import TEMP_FILE_FOLDER
from db import db
from managers.authorization import auth
from managers.insurenece_base import InsurenceManager
from scripts.create_policy_pdf import create_pdf_from_txt
from scripts.radom_number import random_numbers
from services.SES import SES
from services.s3 import S3Service

s3_service = S3Service()
ses = SES()


class EstateInsurenceManager(InsurenceManager):
    @staticmethod
    def create_estate_insurence(insurence_data):
        current_customer = auth.current_user()
        insurence_data["customer_id"] = current_customer.id
        policy_number = f"{str(random_numbers)}"
        insurence_data["policy_number"] = policy_number
        file_name = f"{policy_number}.pdf"
        create_pdf_from_txt(policy_number)
        path_file = os.path.join(TEMP_FILE_FOLDER, file_name)
        try:
            s3_service.upload_file_pdf(
                path_file, file_name, bucket=config("BUCKET_NAME_INSURENCES")
            )
        except Exception as ex:
            raise Exception("Upload pdf failed")
        finally:
            os.remove(path_file)
        ses.send_mail(file_name, current_customer['email'])
        db.session.commit()
