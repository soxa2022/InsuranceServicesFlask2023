import http
import os

import werkzeug
from decouple import config
from flask import make_response
from werkzeug.wrappers import Response
from werkzeug.exceptions import BadRequest

from constants import TEMP_FILE_FOLDER
from db import db
from managers.authorization import auth
from models import RoleType, State, Vehicle, Customer
from scripts.create_policy_pdf import create_pdf_from_txt
from scripts.radom_number import random_numbers
from services.SES import SES
from services.s3 import S3Service
from services.send_email import send_complex_message

s3_service = S3Service()
ses = SES()
TEXT = "Your input information is available"


class InsurenceManager:
    @staticmethod
    def get_insurences(insurence):
        current_customer = auth.current_user()
        role = current_customer.role
        insurences = role_mapper[role](insurence)
        return insurences

    @staticmethod
    def get_employee_insurences(insurence):
        current_user = auth.current_user()
        return insurence.query.filter_by(user_id=current_user.id).all()

    @staticmethod
    def get_accept_insurences(insurence):
        return insurence.query.filter_by(status=State.pending).all()

    @staticmethod
    def get_admin_insurences(inurence):
        return inurence.query.filter_by().all()

    @staticmethod
    def accept_insurence(insurence_id):
        InsurenceManager.validate_status(insurence_id)
        vehicle = Vehicle.query.filter_by(id=insurence_id).first()
        customer = Customer.query.filter_by(id=vehicle.customer_id).first()
        policy_number = f"BG{str(random_numbers())}"
        vehicle.policy_number = policy_number
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
        ses.send_mail(file_name, customer.email)
        Vehicle.query.filter_by(id=insurence_id).update({"status": State.accepted})
        db.session.commit()
        return Response(status=204)

    @staticmethod
    def cancel_insurence(insurence_id):
        InsurenceManager.validate_status(insurence_id)
        vehicle = Vehicle.query.filter_by(id=insurence_id).first()
        customer = Customer.query.filter_by(id=vehicle.customer_id).first()
        send_complex_message(customer.email, TEXT)
        Vehicle.query.filter_by(id=insurence_id).update({"status": State.canceled})
        db.session.commit()
        return Response(status=204)

    @staticmethod
    def validate_status(insurence_id):
        insurence_ = Vehicle.query.filter_by(id=insurence_id).first()
        if not insurence_:
            raise BadRequest("Insurence not exist")
        if not insurence_.status == State.pending:
            raise BadRequest("Can not change processed insurence")

    @staticmethod
    def delete_insurence(pk):
        InsurenceManager.validate_status(pk)
        Vehicle.query.filter_by(id=pk).update({"is_deleted": True})
        return Response(status=204)

    @staticmethod
    def update_insurence(pk):
        InsurenceManager.validate_status(pk)
        # TODO: Add functionality


role_mapper = {
    RoleType.customer: InsurenceManager.get_employee_insurences,
    RoleType.admin: InsurenceManager.get_admin_insurences,
    RoleType.employee: InsurenceManager.get_accept_insurences,
}
