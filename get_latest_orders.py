import os
import requests
import time
import hashlib
import hmac

# Replace placeholders with your actual credentials
STORE_CODE = os.environ.get('HKTVMALL_STORE_CODE', 'your_store_code')
API_KEY = os.environ.get('HKTVMALL_API_KEY', 'your_api_key')
PRIVATE_KEY = os.environ.get('HKTVMALL_PRIVATE_KEY', 'your_private_key')

# Base URL for HKTVmall API (adjust if different)
BASE_URL = 'https://corp.hktvmall.com/openapi'

# API endpoint to list orders
ENDPOINT = '/order/list'

# Number of orders to fetch
LIMIT = 10

def sign_request(api_key: str, private_key: str, timestamp: str, body: str = '') -> str:
    """Return HMAC SHA256 signature for HKTVmall API."""
    message = f'{api_key}{timestamp}{body}'.encode('utf-8')
    signature = hmac.new(private_key.encode('utf-8'), message, hashlib.sha256).hexdigest()
    return signature

def get_latest_orders():
    timestamp = str(int(time.time() * 1000))
    body = ''
    signature = sign_request(API_KEY, PRIVATE_KEY, timestamp, body)

    headers = {
        'X-API-KEY': API_KEY,
        'X-SIGNATURE': signature,
        'X-TIMESTAMP': timestamp,
        'Content-Type': 'application/json'
    }

    params = {
        'store_code': STORE_CODE,
        'limit': LIMIT
    }

    response = requests.get(BASE_URL + ENDPOINT, headers=headers, params=params, timeout=10)
    response.raise_for_status()
    return response.json()

if __name__ == '__main__':
    try:
        orders = get_latest_orders()
        print('Latest orders:')
        print(orders)
    except requests.HTTPError as e:
        print(f'HTTP error: {e.response.status_code} - {e.response.text}')
    except Exception as e:
        print(f'An error occurred: {e}')
