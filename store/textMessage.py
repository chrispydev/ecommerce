from twilio.rest import Client

def send_message():
    account_sid = "AC47b7f0da57ec0587eb6ba5fce3bf8913"
    auth_token = "a8e3c32b436d922dd4f319a0cdc12695"
    client = Client(account_sid, auth_token)

    message = client.messages.create(from_="+16092566864", body="Thank you for ordering", to="+233553782097")

    print(f"message sent with message.sid:{message.sid}")
