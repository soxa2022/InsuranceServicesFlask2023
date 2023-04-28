import logging
import os
import time

from flask_apscheduler import APScheduler
from sqlalchemy.sql import text

from constants import TEMP_FILE_FOLDER
from db import db
from services.send_email import send_complex_message

scheduler = APScheduler()


class Config:
    def __init__(self):
        logging.basicConfig(
            filename=os.path.join(TEMP_FILE_FOLDER, "scheduler.log"),
            level=logging.INFO,
            format="%(asctime)s %(levelname)s %(message)s",
        )


def schedule(app):
    scheduler.api_enabled = True
    scheduler.init_app(app)
    scheduler.start()
    scheduler.add_job(id="my_task", func=my_task, trigger="interval", seconds=5)


def my_task():
    with scheduler.app.app_context():
        Config()

        result = db.session.execute(
            text(
                "SELECT email,policy_number FROM get_data GROUP BY policy_number,email"
            )
        ).all()
        if result:
            for row in result:
                email = [row[0]]
                policy_number = row[1]
                message = (
                    f"Your insurence policy number {policy_number} expires in 10 days"
                )
                try:
                    if policy_number:
                        print(message)
                        # send_complex_message(email, message)
                        time.sleep(5)
                except Exception as e:
                    logging.error(f"Failed to run task: {e}")
        db.session.commit()
