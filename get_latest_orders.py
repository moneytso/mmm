import os
import time
from datetime import datetime, timedelta
import requests
import jwt

STORE_CODE = os.environ.get('HKTVMALL_STORE_CODE')
API_KEY = os.environ.get('HKTVMALL_API_KEY')
PRIVATE_KEY = os.environ.get('HKTVMALL_PRIVATE_KEY')

BASE_URL = "https://merchant-oapi.shoalter.com"
ORDERS_ENDPOINT = "/oapi/api/order/orders"
DETAILS_ENDPOINT = "/oapi/api/order/details"
PAGE_SIZE = 10


def create_token(api_key: str, private_key: str) -> str:
    payload = {
        "sub": "shoalter",
        "name": "shoalter",
        "iat": int(time.time()),
        "x-api-key": api_key,
    }
    return jwt.encode(payload, private_key, algorithm="RS256")


def request_orders(token: str) -> dict:
    now = datetime.utcnow()
    start = now - timedelta(days=30)
    params = {
        "orderDateStart": start.strftime("%Y-%m-%d %H:%M:%S"),
        "orderDateEnd": now.strftime("%Y-%m-%d %H:%M:%S"),
        "pageSize": PAGE_SIZE,
        "page": 1,
    }
    headers = {
        "Content-Type": "application/json",
        "x-auth-token": token,
        "storeCode": STORE_CODE or "",
        "platformCode": "HKTV",
        "businessType": "eCommerce",
    }
    response = requests.get(BASE_URL + ORDERS_ENDPOINT, headers=headers, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def request_details(token: str, order_numbers: list) -> dict:
    headers = {
        "Content-Type": "application/json",
        "x-auth-token": token,
        "storeCode": STORE_CODE or "",
        "platformCode": "HKTV",
        "businessType": "eCommerce",
    }
    payload = {"subOrderNumbers": order_numbers}
    response = requests.get(BASE_URL + DETAILS_ENDPOINT, headers=headers, json=payload, timeout=10)
    response.raise_for_status()
    return response.json()


def main():
    if not all([STORE_CODE, API_KEY, PRIVATE_KEY]):
        raise EnvironmentError("Please set HKTVMALL_STORE_CODE, HKTVMALL_API_KEY and HKTVMALL_PRIVATE_KEY")

    token = create_token(API_KEY, PRIVATE_KEY)
    orders_resp = request_orders(token)
    order_numbers = orders_resp.get("data", {}).get("subOrderNumbers", [])
    if not order_numbers:
        print("No orders found")
        return

    details_resp = request_details(token, order_numbers)
    print(details_resp)


if __name__ == "__main__":
    main()
