# HKTVmall Latest Orders Script

This repository includes a Python script for fetching your store's most recent orders from HKTVmall's official API.

## Requirements
- Python 3.8+
- `requests` and `PyJWT` libraries

Install dependencies with:
```bash
pip install requests PyJWT
```

## Usage
Set your credentials as environment variables:
```bash
export HKTVMALL_STORE_CODE="your_store_code"
export HKTVMALL_API_KEY="your_uuid"
export HKTVMALL_PRIVATE_KEY="path_or_key"
```
Run the script:
```bash
python get_latest_orders.py
```

The script generates a token using your private key, retrieves the latest ten orders from the past 30 days, and prints the order details as JSON.
