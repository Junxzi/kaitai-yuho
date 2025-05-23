import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("EDINET_API_KEY")
if not API_KEY:
    raise ValueError("EDINET_API_KEY is not set in the .env file")