import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))

INVENTARIZATION_SPREADSHEET_ID = str(os.getenv("INVENTARIZATION_SPREADSHEET_ID"))
PHONE_SPREADSHEET_ID = str(os.getenv("PHONE_SPREADSHEET_ID"))

CREDENTIAL_FILE = str(os.getenv("CREDENTIAL_FILE"))

DB_FILE_PATH = str(os.getenv("DB_FILE_PATH"))

LOG_FILE = str(os.getenv("LOG_FILE"))

CHANNEL_URL = str(os.getenv("CHANNEL_URL"))

IT_SUPPORT_TABLE = str(os.getenv("IT_SUPPORT_TABLE"))
IT_SUPPORT_FORM = str(os.getenv("IT_SUPPORT_FORM"))

admins = [
    os.getenv("ADMIN_ID"),
]

ip = os.getenv("ip")
