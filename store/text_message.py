import json
import http.client as httpClient

def send_text_message(receiver, message):
    try:
        host = "api.smsonlinegh.com"
        requestURI = "http://api.smsonlinegh.com/v5/message/sms/send"
        apiKey = "31fafe25761c91faa93cbaa6c08bb712bb627e9705f77c0e4d434b132084906f"

        headers = dict()
        headers["Host"] = host
        headers["Content-Type"] = "application/json"
        headers["Accept"] = "application/json"
        headers["Authorization"] = f"key {apiKey}"

        # message data
        msgData = dict()
        msgData["text"] = message
        msgData["type"] = 0
        msgData["sender"] = "RemGee"
        msgData["destinations"] = ['0553782097']

        httpConn = httpClient.HTTPConnection(host)
        httpConn.request("POST", requestURI, json.dumps(msgData), headers)

        # get the reponse
        response = httpConn.getresponse()

        # check the status
        status = response.status

        if status == 200:
            responseData = response.read()
            print(responseData)
        else:
            print("Request was unsuccessful")

    except Exception as e:
        print(str(e))
        return e
