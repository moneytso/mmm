# HKTVmall Latest Orders Script

This repository includes a small Python script to retrieve the latest orders from HKTVmall using their open API. Set your store credentials as environment variables and run the script.

## Usage

```bash
export HKTVMALL_STORE_CODE="your_store_code"
export HKTVMALL_API_KEY="your_api_key"
export HKTVMALL_PRIVATE_KEY="your_private_key"
python get_latest_orders.py
```

The script will request the latest 10 orders and print them as JSON.
