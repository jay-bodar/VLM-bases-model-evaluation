import os
import aip_sdk as aip
from dotenv import load_dotenv

# 1. Load your credentials and connect to the platform
load_dotenv()
BASE_URL = os.environ.get("AIP_BASE_URL", "http://localhost:8010")
aip.init(
    BASE_URL, 
    username=os.environ.get("AIP_USERNAME"), 
    password=os.environ.get("AIP_PASSWORD")
)

print("Connected! Fetching available metrics...\n")

# 2. Get ONLY the metrics that work for text/LLM tasks
text_metrics = aip.ops.list_metrics(schema="gdi_text_v1")

print("--- AVAILABLE TEXT METRICS ---")
for op in text_metrics:
    print(f"Name: {op['name']}")
    print(f"Description: {op.get('description', 'No description provided')}")
    print("-" * 30)