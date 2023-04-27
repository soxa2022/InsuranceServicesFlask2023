import os

from decouple import config

from constants import TEMP_FILE_FOLDER
from db import db
from managers.authorization import auth
from managers.insurenece_base import InsurenceManager
from models import Vehicle
from services.s3 import S3Service
from utils.helpers import decode_photo

s3_service = S3Service()


class VehicleInsurenceManager(InsurenceManager):
    @staticmethod
    def create_vehicle_insurence(insurence_data):
        current_customer = auth.current_user()
        insurence_data["customer_id"] = current_customer.id
        photo_into_str = insurence_data.pop("photo")
        extension = insurence_data.pop("extension")
        photo_name = f"{insurence_data['talon_number']}.{extension}"
        path_photo_file = os.path.join(TEMP_FILE_FOLDER, photo_name)
        decode_photo(path_photo_file, photo_into_str)

        try:
            url = s3_service.upload_file_pic(
                path_photo_file, photo_name, bucket=config("BUCKET_NAME_TALONS")
            )
        except Exception as ex:
            raise Exception("Upload photo failed")
        finally:
            os.remove(path_photo_file)

        insurence_data["talon_photo"] = url
        insurence = Vehicle(**insurence_data)
        db.session.add(insurence)
        db.session.commit()
        return insurence
