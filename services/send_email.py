import os

import requests
from decouple import config

from constants import TEMP_FILE_FOLDER

path_file = os.path.join(TEMP_FILE_FOLDER, "test.txt")

emails = [config("TEST_EMAIL")]


def send_complex_message(mails, text):
    res = requests.post(
        f"https://api.mailgun.net/v3/{config('MY_MAILGUN_DOMAIN')}/messages",
        auth=("api", config("EMAIL_API_KEY")),
        files=[("attachment", ("test.txt", open(path_file, "rb").read()))],
        data={
            "from": "Insurenes.Services@momoshe.com",
            "to": mails,
            "subject": "Hello from the best services",
            "text": text,
        },
    )
    return res.status_code


# if __name__ == "__main__":
#     print(send_complex_message(emails).status_code)
