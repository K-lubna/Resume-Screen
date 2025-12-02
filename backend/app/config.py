# backend/app/config.py
import os
from dotenv import load_dotenv
load_dotenv()

PORT = int(os.getenv("PORT", 8000))
MODEL_NAME = os.getenv("SENTENCE_MODEL", "all-mpnet-base-v2")
