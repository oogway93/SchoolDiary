import os

from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.environ.get('API_TOKEN')
ADMIN_ID1 = os.environ.get('ADMIN_ID1')
ADMIN_ID2 = os.environ.get('ADMIN_ID2')
MONGO_USER = os.environ.get('MONGO_USER')
MONGO_PASS = os.environ.get('MONGO_PASS')

MONGO_url = f"mongodb+srv://{MONGO_USER}:{MONGO_PASS}@cluster0.tp39w0i.mongodb.net/?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE"
