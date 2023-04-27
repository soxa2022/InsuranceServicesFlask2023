import logging
import os
import time

from flask_apscheduler import APScheduler

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
        # print('Job 1 executed')
        Config()
        try:
            result = db.session.execute("SELECT * FROM reminder_view").all()
            if result:
                for row in result:
                    email = [row[0]]
                    policy_number = row[1]
                    text = f"Your insurence policy number {policy_number} expires in 10 days"
                    send_complex_message(email, text)
                    time.sleep(5)
            db.session.commit()
        except Exception as e:
            logging.error(f"Failed to run task: {e}")
