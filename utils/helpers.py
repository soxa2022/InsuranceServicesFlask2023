import base64

from werkzeug.exceptions import BadRequest


def decode_photo(path, encoded_string):
    with open(path, "wb") as f:
        try:
            f.write(base64.b64decode(encoded_string.encode("utf-8")))
        except Exception as ex:
            raise BadRequest("Invalid photo encoding")


def encode_image(file):
    with open(file, "rb") as i:
        try:
            encoded_string = base64.b64encode(i.read()).decode("utf-8")
        except Exception as ex:
            raise BadRequest("Invalid photo encoding")
    return encoded_string


encoded_photo = ""
