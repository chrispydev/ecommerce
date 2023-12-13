import http.client as httpClient
import json

# API host domain
host = "api.smsonlinegh.com"

# API request URL
requestURL = "http://api.smsonlinegh.com/v5/account/balance"

# set up the request headers
headers = dict()
headers["Host"] = host
headers["Content-Type"] = "application/json"
headers["Accept"] = "application/json"
headers[
    "Authorization"
] = "key 31fafe25761c91faa93cbaa6c08bb712bb627e9705f77c0e4d434b132084906f"

httpConn = httpClient.HTTPConnection(host)
httpConn.request("POST", requestURL, None, headers)

# get the reponse
response = httpConn.getresponse()

if response.status == 200:
    # Read the response content
    response_content = response.read().decode("utf-8")

    # Parse the JSON response
    json_response = json.loads(response_content)

    # Access the "data" field in the JSON response
    data = json_response["data"]

    print(data)
else:
    print("Request was unsuccessful")
