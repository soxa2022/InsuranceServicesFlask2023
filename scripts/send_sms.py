from decouple import config


def send_sms(phone):
    import pprint
    import bsg_restapi as api

    client = api.SMSAPI(config={"api_key": config("API_KEY")})
    result = client.send(
        message=api.SMSMessage(body="test message text"),
        recipients=api.Recipient(380967770002),
    )
    print("Result of SMS sending:\n{}".format(pprint.pformat(result)))
    # getting status of SMS
    status = client.get_status(result["reference"])
    print(
        "Current SMS status result for reference {}: \n{}".format(
            result["reference"], pprint.pformat(status, indent=4)
        )
    )
