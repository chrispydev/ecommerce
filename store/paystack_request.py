import requests

# Set your Paystack API key
api_key = 'sk_test_195e9139ee9d2f5846323c2e0e039858fbe4c390'
# Provide the reference ID of the transaction you want to fetch

def get_payment_method(reference):
    # reference_id = '3408295699'
    reference_id = reference

    # Set the API endpoint
    endpoint = f'https://api.paystack.co/transaction/{reference_id}'

    # Set the request headers
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    # Send GET request to the API
    response = requests.get(endpoint, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        payment_method = data['data']['authorization']['authorization_code']
        payment_channel = data['data']['authorization']['channel']
        return payment_channel
    else:
        print("Error:", response.text)
        payment_channel = 'mobile_money'
        return payment_channel