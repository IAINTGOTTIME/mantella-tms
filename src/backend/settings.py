from dotenv import load_dotenv
import os

load_dotenv("ENV/.env")

LEVEL = os.getenv("LEVEL")
SECRET = os.getenv("SECRET")
EMAIL_PASS = os.getenv("EMAIL_PASS")





