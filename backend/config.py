import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_URI = os.getenv('MONGO_URI')
    FLASK_PORT = int(os.getenv("FLASK_PORT", 5000))
