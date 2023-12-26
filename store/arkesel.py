import requests

message = 'This is a text message'
phoneNumber = '+233553782097'
senderId = 'Remgee'

res = requests.get(f'https://sms.arkesel.com/sms/api?action=send-sms&api_key=U3ZxUmpXQ0ZtSFJsSXZhd2NMYk0&to={phoneNumber}&from={senderId}&sms={message}')

print(res.text)