import os
import requests
from weird_history.pipeline.config import CARTESIA_API_KEY
headers = {"X-API-Key": CARTESIA_API_KEY, "Cartesia-Version": "2024-06-10"}
resp = requests.get("https://api.cartesia.ai/voices", headers=headers)
print("\n".join([f"{v['id']} - {v['name']} ({v.get('language', 'en')})" for v in resp.json() if "es" in v.get('language', 'en') or v.get('is_public')]))
