from email_validator import validate_email, EmailNotValidError
from marshmallow import ValidationError
from password_strength import PasswordPolicy

policy = PasswordPolicy.from_names(
    uppercase=1,  # need min. 1 uppercase letters
    numbers=1,  # need min. 1 digits
    special=1,  # need min. 1 special characters
    nonletters=1,  # need min. 1 non-letter characters (digits, specials, anything)
)


def validate_password(value):
    errors = policy.test(value)
    if errors:
        raise ValidationError("Not a valid password")


def check_email(email):
    try:
        validate_email(email)
    except EmailNotValidError as e:
        raise ValidationError(str(e))


# [БСВ Консултинг - Контролни цифри ползвани в България](http://bsv-bg.com/контролни-цифри-ползвани-в-българия)


CONTROLS_DIGITS = [2, 4, 8, 5, 10, 9, 7, 3, 6]


def check_egn(value):
    gender = "m" if int(value[8]) % 2 == 0 else "f"

    day = int(value[4:6])
    month = int(value[2:4])
    year = int(value[0:2])

    if month > 40:
        year += 2000
        month -= 40
    elif month > 20:
        year += 1800
        month -= 20
    else:
        year += 1900

    birthday = {"year": year, "month": month, "day": day}
    sum_ = 0

    for i in range(len(value) - 1):
        sum_ += int(value[i]) * CONTROLS_DIGITS[i]

    mod = sum_ % 11
    mod = mod if mod < 10 else 0

    if not mod == int(value[9]):
        raise ValidationError("Not a valid EGN")


CONTROLS_DIGITS_9_1 = [1, 2, 3, 4, 5, 6, 7, 8]
CONTROLS_DIGITS_9_2 = [3, 4, 5, 6, 7, 8, 9, 10]
CONTROLS_DIGITS_13_1 = [2, 7, 3, 5]
CONTROLS_DIGITS_13_2 = [4, 9, 5, 7]


def check_bulstat(value):
    val = [int(char) for char in value]
    sum_ = 0
    for i in range(8):
        sum_ += val[i] * CONTROLS_DIGITS_9_1[i]
    mod = sum_ % 11
    if mod > 9:
        sum_ = 0
        for i in range(8):
            sum_ += val[i] * CONTROLS_DIGITS_9_2[i]
        mod = sum_ % 11
        mod = 0 if mod > 9 else mod
    if len(value) == 9:
        if not mod == val[8]:
            raise ValidationError("Not a valid Bulstat")
        return
    val[8] = mod
    sum_ = 0
    for i in range(8, 12):
        sum_ += val[i] * CONTROLS_DIGITS_13_1[i - 8]
    mod = sum_ % 11
    if mod > 9:
        sum_ = 0
        for i in range(8, 12):
            sum_ += val[i] * CONTROLS_DIGITS_13_2[i - 8]
        mod = sum_ % 11
        mod = 0 if mod > 9 else mod
    if not mod == val[12]:
        raise ValidationError("Not a valid Bulstat")


def is_valid(value):
    if not isinstance(value, str):
        raise ValidationError(f"{value} is not of type string!")
    if not value.isdigit():
        raise ValidationError(f"{value} not contains only digits!")
    value = value.replace(" ", "")
    length = len(value)
    if length == 9 or length == 13:
        return check_bulstat(value)
    elif length == 10:
        return check_egn(value)
    else:
        raise ValueError(f"{value} with size {length} is not valid EGN or Bulstat!")
