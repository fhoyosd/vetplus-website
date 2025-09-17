import os
from dotenv import load_dotenv

load_dotenv()

RECAPTCHA_SECRET_KEY = os.getenv("RECAPTCHA_SITE_KEY")