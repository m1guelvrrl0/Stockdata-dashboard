import os
from dotenv import load_dotenv

load_dotenv()

BACKEND = 'yahoo'
API_KEY = os.getenv("API_KEY")
DB_URI = os.getenv("DATABASE_URI")
